import asyncio
from mipa.ext import commands
from mipa.ext.commands.bot import Bot
from mipa.ext.commands.context import Context
from mipac.models import NotificationPollEnd
from cogs.modules.youna import Youna

class GameCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.youna = None

    @commands.mention_command(text='/noyouna')
    async def noyouna_setting(self, ctx: Context):
        if ctx.message.content.endswith('/noyouna'):
            await ctx.message.api.action.reply(f'「のようなゲーム」の募集を始めます(開催者:{ctx.message.author.username})')
            self.youna = Youna(organizer=ctx.message.author)

    @commands.mention_command(text='/join_noyouna')
    async def noyouna_join(self, ctx: Context):
        await self._noyouna_join(ctx)

    @commands.mention_command(text='/noyouna_join')
    async def noyouna_join2(self, ctx: Context):
        await self._noyouna_join(ctx)

    async def _noyouna_join(self, ctx: Context):
        if self.youna.status == self.youna.STATUS_INIT:
            message = self.youna.join(ctx.message.author)
            if self.youna.status == self.youna.STATUS_START:
                note = await ctx.message.api.action.reply(f'最大参加人数({len(self.youna.members)})に到達したので、ゲームを開始します')
                print(message.message + '\r\ncw:' + message.cw_message)
                await note.api.action.reply(content=message.cw_message, cw=message.message)
            else:
                await ctx.message.api.action.reply(message.message)
        else:
            await ctx.message.api.action.reply('途中参加は不可能です')

    @commands.mention_command(text='/noyouna_start')
    async def noyouna_start(self, ctx: Context):
        if self.youna.status == self.youna.STATUS_INIT:
            message = self.youna.start()
            if self.youna.status == self.youna.STATUS_START:
                note = await ctx.message.api.action.reply(f'ゲームを開始します(参加人数:{len(self.youna.members)})')
                print(message.message + '\r\ncw:' + message.cw_message)
                await note.api.action.reply(content=message.cw_message, cw=message.message)
            else:
                await ctx.message.api.action.reply(f'開催できませんでした。\r\n`<このbotへのメンション> /noyouna_join`で参加してもらってください(参加人数:{len(self.youna.members)})')

    @commands.Cog.listener()
    async def on_poll_end(self, notice: NotificationPollEnd):
        print(notice.note.poll)
        test = notice.note.poll
        for choice in test.choices:
            print(choice.votes, choice.text)

async def setup(bot: Bot):
    await bot.add_cog(GameCog(bot))