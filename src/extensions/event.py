import discord
from discord.ext import commands, tasks
import importlib
import config
from itertools import cycle

class EventCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        importlib.reload(config)
        self.status = cycle(config.BOT_STATUS)
        self.change_bot_status.start()

    @tasks.loop(seconds=20)
    async def change_bot_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status)))

    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx: commands.Context, error):
        mention = f"<@!{ctx.author.id}>"
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(f"{mention} 찾을 수 없는 유저입니다.")
        if isinstance(error, commands.errors.ExtensionNotLoaded):
            await ctx.send(f"{mention} 찾을 수 없는 **Extension**입니다.")
        # if isinstance(error, commands.errors.CommandInvokeError):
        #     await ctx.send(f"{mention} 알수 없는 오류입니다.")
        if isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.send("봇보다 권한이 높거나, 봇이 권한이 없어 명령어를 사용할수 없습니다.")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send(f"{mention} 당신은 권한이 없습니다.")
        if isinstance(error, commands.errors.ArgumentParsingError):
            await ctx.send(f"{mention} 양식에 맞게 적어주세요.")

def setup(bot):
    bot.add_cog(EventCog(bot))