from mipa.ext import commands
from mipa.ext.commands.bot import Bot
from mipa.ext.commands.context import Context
from mipac.models.note import Note
from .modules.weather import Weather
import re

class UtilitycogCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.weather = Weather()

    @commands.mention_command(regex=r'[Tt]enki (.+)')
    async def tenki(self, ctx: Context, tenki:str):
        return await self._check_weather(tenki=tenki, ctx=ctx)

    @commands.mention_command(regex='[Ww]eather (.+)')
    async def weather(self, ctx: Context, tenki:str):
        return await self._check_weather(tenki=tenki, ctx=ctx)

    @commands.Cog.listener()
    async def on_note(self, note: Note):
        print(note.text)

        # Weather対応
        weather_match = re.match('^/(([Tt]enki)|([Ww]eather)) (.+)\n?', note.text)
        if weather_match and len(weather_match.groups()) == 4:
            print(weather_match.groups())
            return await self._check_weather(tenki=weather_match.group(4), note=note)

    async def _check_weather(self, tenki:str, ctx: Context=None, note: Note=None):
        weather_result = await self.weather.getWeather(tenki)
        message = f'''{weather_result.get('text')}'''
        if weather_result.get('sub'):
            message += f'''\n{weather_result.get('sub')}'''
        if ctx:
            await ctx.message.api.action.reply(message)
        elif note:
            await note.api.action.reply(message)

async def setup(bot: Bot):
    await bot.add_cog(UtilitycogCog(bot))