import asyncio
from aiohttp import ClientWebSocketResponse
#from mipac import Note
#from mipac.models.notification import NotificationNote
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

    async def _connect_channel(self):
        await self.router.connect_channel(['main', 'local'])

    async def on_ready(self, ws: ClientWebSocketResponse):
        print('Logged in ', self.user.username)
        await self._connect_channel()
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)

    async def on_reconnect(self, ws: ClientWebSocketResponse):
        print('Disconnected from server. Will try to reconnect.')
        await self._connect_channel()

    # async def on_mention(self, notice: NotificationNote):
        # When using this event, if you use MENTION_COMMAND, you must call this method for it to work.
        # await self.progress_command(notice)

    # async def on_note(self, note: Note):
        # print(note.author.username, note.content)

if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start(
        url=settings.MISSKEY_STREAMING_URL
        , token=settings.MISSKEY_TOKEN
        , debug=True
        , reconnect=True
        ,timeout=1000)
    )
