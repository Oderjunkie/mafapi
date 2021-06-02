# {
#   id: 123
#   username: otesunki
#   nickname: +_+
#   badges: [mod, admin]
#   color: #F00
#   wins: 12
#   loss: 6
#   rating: 24
#   antirating: 3
#   permlevel: 4
# }

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from asyncinit import asyncinit


@asyncinit
class LookupDB:
    async def __init__(self):
        self.client = AsyncIOMotorClient("mongodb+srv://plainuser:SMCbzdmteZYpWd1E@cluster0.guqu1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        
