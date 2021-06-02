import asyncio
import logging
from asyncinit import asyncinit
from motor.motor_asyncio import AsyncIOMotorClient
from mafapi.session import Session
from mafapi.connection import Connection

def traceback(e):
    print('Custom traceback:')
    print('File "{}", line {}, in {}'.format(e.__traceback__.tb_frame.f_code.co_filename,
                                             e.__traceback__.tb_frame.f_code.co_firstlineno,
                                             e.__traceback__.tb_frame.f_code.co_name))
    with open(e.__traceback__.tb_frame.f_code.co_filename) as f:
        lines = f.readlines()
        line = e.__traceback__.tb_lineno-1
        funcline = e.__traceback__.tb_frame.f_code.co_firstlineno-1
        print('    {}\t{}'.format(funcline, lines[funcline][:-1]))
        print('    {}\t{}'.format(line-1, lines[line-1][:-1]))
        print('>>> {}\t{}'.format(line,   lines[line][:-1]))
        print('    {}\t{}'.format(line+1, lines[line+1][:-1]))
        print('{}: {}'.format(str(type(e))[8:-2], str(e)))
        f.close()

@asyncinit
class BotBase:
    async def __init__(self, config):
        self.client = AsyncIOMotorClient(config.MONGODB)
        self.session = await Session()
        await self.session.login(config.USERNAME, config.PASSWORD)
        self.ws = None
        if config.ROOMID:
            self.ws = await self.session.joinRoomById(config.ROOMID)
            logging.info('Joined https://mafia.gg/game/%s', config.ROOMID)
        else:
            roomid = await self.session.createRoom(config.ROOMNAME, config.UNLISTED)
            logging.info('Joined https://mafia.gg/game/%s', roomid)
            self.ws = await self.session.joinRoomById(roomid)
        self.endGameData = {}
        await self._extended_init__()
    async def _extended_init__(self):
        pass
    async def send(self, string):
        return await self.ws.sendchat(string)
    async def sendPacket(self, packet):
        if packet['type']=='newGame':
            logging.info('Joined https://mafia.gg/game/%s', packet['roomId'])
        return await self.ws.send(packet)
    async def updateOpts(self):
        return await self.ws.send(self.ws.options)
    async def run(self):
        await self._on_help(None, [])
        while True:
            data = await self.ws.get()
            asyncio.create_task(self.parse_packet(data))
    async def parse_packet(self, packet):
        await self.side_effects(packet)
        filtered = await self.filter_packet(packet)
        if filtered:
            #userobj = filtered[0]
            #command = filtered[1]
            #args = filtered[:2]
            userobj, command, *args = filtered
            return await self.exec_command(userobj, command, args)
        return
    async def side_effects(self, packet):
        if packet['type']=='userJoin':
            user = await self.client.mafiagg.users.find_one({
                'id': packet['userId']
            })
            if not user:
                userobj = (await self.session.getUser(packet['userId']))[0]
                user = {
                    'id': userobj.id,
                    'username': userobj.username,
                    'nickname': userobj.username,
                    'badges': [],
                    'color': '#FFFFFF',
                    'wins': 0,
                    'loss': 0,
                    'rating': 0,
                    'antirating': 0,
                    'permlevel': 0
                }
                await self.client.mafiagg.users.insert_one(user)
            generatedname = ''
            if user['nickname']==user['username']:
                generatedname = '{}'.format(user['username'])
            else:
                generatedname = '{} ({})'.format(user['nickname'], user['username'])
            def limit(string):
                if len(string)<50:
                    return string
                return string[:50]+'...'
            if len(user['badges'])>0:
                generatedname += ' ' + limit(' '.join(map('[{}]'.format, user['badges'])))
            await self._greet(user, generatedname)
        if packet['type']=='userQuit':
            user = await self.client.mafiagg.users.find_one({
                'id': packet['userId']
            })
            generatedname = ''
            if user['nickname']==user['username']:
                generatedname = '{}'.format(user['username'])
            else:
                generatedname = '{} ({})'.format(user['nickname'], user['username'])
            def limit(string):
                if len(string)<50:
                    return string
                return string[:50]+'...'
            if len(user['badges'])>0:
                generatedname += ' ' + limit(' '.join(map('[{}]'.format, user['badges'])))
            await self._goodbye(generatedname)
        if packet['type']=='endGame': # insert avengers end game referece here
            await self._game_end_packet(packet)
        if packet['type']=='system' and packet['message'].startswith('Winning teams:'):
            await self._game_finish(packet['message'])
    async def edit_attribute_of_userobj(self, userobj, updated_fields):
        return await self.client.mafiagg.users.update_one(
            { 'id': userobj.id, 'username': userobj.username },
            { '$set': updated_fields }
        )
    async def edit_attribute_of_user_with_filter(self, filters, updated_fields):
        return await self.client.mafiagg.users.update_one(
            filters,
            { '$set': updated_fields }
        )
    async def edit_attribute_of_user(self, user, updated_fields):
        return await self.client.mafiagg.users.update_one(
            user,
            { '$set': updated_fields }
        )
    async def find_user_with_filter(self, filters):
        return await self.client.mafiagg.users.find_one(filters)
    async def filter_packet(self, packet):
        if packet['type']!='chat': return []
        if packet['from']['userId'] == self.session.user.id: return []
        msg = packet['message'].strip()
        if not msg.startswith('!'): return []
        command, *args = msg.split(' ')
        command = command.lower()
        return [(await self.session.getUser(packet['from']['userId']))[0], command[1:], *args]
    async def exec_command(self, userobj, command, args):
        func = None
        try:
            func = getattr(self, '_on_{}'.format(command))
        except AttributeError as e:
            return await self._invalid_(userobj, command, args)
        finally:
            return await func(userobj, args)
            #func = eval('self.___{}'.format(command))
            #logging.debug('%r: %r', type(e), e.args[0])
    async def _game_finish(self, winningteams):
        pass
    async def _game_end_packet(self, packet):
        pass
    async def _greet(self, generatedname):
        pass
    async def _invalid_(self, userobj, command, args):
        pass
    async def _error_badge_missing(self, userobj, user, badge):
        pass
    async def _error_badge_present(self, userobj, user, badge):
        pass
    async def _error_perm_missing(self, userobj, user, perm):
        pass
    async def _error_user_mismatch(self, userobj, user, usernamereq):
        pass
