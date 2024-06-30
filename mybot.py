import asyncio
from aiohttp import ClientWebSocketResponse
#from mipac import Note
from mipa.ext.commands.bot import Bot
from cogs.modules import settings

# 読み込むCogの名前を格納
INITIAL_EXTENSIONS = [
    'cogs.basiccog'
    ,'cogs.utilitycog'
    # ,'cogs.gamecog'
]

class MyBot(Bot):
    def __init__(self):
        super().__init__()

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self.router.connect_channel(['main', 'local'])
        print('Logged in ', self.user.username)
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)

    # async def on_note(self, note: Note):
        # print(note.author.username, note.content)

if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start(settings.MISSKEY_STREAMING_URL, settings.MISSKEY_TOKEN))
