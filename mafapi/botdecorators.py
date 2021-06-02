def badge_req(badge, useDB=False):
    def returned(func):
        async def replacementfunc(self, userobj, args):
            user = await self.client.mafiagg.users.find_one({
                'id': userobj.id,
                'username': userobj.username
            })
            if badge in user['badges']:
                return await func(self, user if useDB else userobj, args)
            else:
                return await self._error_badge_missing(userobj, user, badge)
        return replacementfunc
    return returned

def badge_ban(badge, useDB=False):
    def returned(func):
        async def replacementfunc(self, userobj, args):
            user = await self.client.mafiagg.users.find_one({
                'id': userobj.id,
                'username': userobj.username
            })
            if badge in user['badges']:
                return await self._error_badge_present(userobj, user, badge)
            else:
                return await func(self, user if useDB else userobj, args)
        return replacementfunc
    return returned

def perm_req(perm, useDB=False):
    def returned(func):
        async def replacementfunc(self, userobj, args):
            user = await self.client.mafiagg.users.find_one({
                'id': userobj.id,
                'username': userobj.username
            })
            if user['permlevel'] < perm:
                return await func(self, user if useDB else userobj, args)
            else:
                return await self._error_perm_missing(userobj, user, perm)
        return replacementfunc
    return returned

def locked_to(username, useDB=False):
    def returned(func):
        async def replacementfunc(self, userobj, args):
            user = await self.client.mafiagg.users.find_one({
                'id': userobj.id,
                'username': userobj.username
            })
            if userobj.username != username:
                return await func(self, user if useDB else userobj, args)
            else:
                return await self._error_user_mismatch(userobj, user, username)
        return replacementfunc
    return returned

def use_database(func):
    async def replacementfunc(self, userobj, args):
        user = await self.client.mafiagg.users.find_one({
            'id': userobj.id,
            'username': userobj.username
        })
        return await func(self, user, args)
    return replacementfunc

#def unionreq(*funcs):
#    def returned
