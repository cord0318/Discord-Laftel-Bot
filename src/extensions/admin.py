import discord, psutil, config, datetime, os
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="reload", aliases=["리로드", "Reload"])
    async def reload(self, ctx: commands.Context, path=None) -> None:
        if ctx.author.id in config.OWNER_ID:
            if path == "*" or path == "." or path == None:
                msg = await ctx.send(f"**모든 extensions**을 리로드 하는중...")
                for path in config.EXTENSION_LIST:
                    self.bot.reload_extension(path)
            else:
                msg = await ctx.send(f"`extensions`의 **{path}**를 리로드 하는중...")
                self.bot.reload_extension(f"extensions.{path}")
            await msg.edit(content=":white_check_mark: **성공적으로 모듈을 리로드 하였습니다!**")
        else:
            await ctx.send(":x: 당신은 이 봇의 **OWNER**가 아닙니다!")

    @commands.command(name="uptime", aliases=["업타임", "Uptime"])
    async def uptime(self, ctx: commands.Context):
        if ctx.author.id in config.OWNER_ID:
            uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.Process(os.getpid()).create_time())
            await ctx.send(f"<@!{config.BOT_ID}> uptime : **{uptime}**")
        else:
            await ctx.send(f":x: 당신은 이 봇의 **OWNER**가 아닙니다!")

    @commands.command(name="list_extension", aliases=["기능리스트", "list"])
    async def list_extension(self, ctx: commands.Context):
        if ctx.author.id in config.OWNER_ID:
            embed = discord.Embed(title="[ EXTENSION LIST ]")
            embed.description = "***" + ", ".join(config.EXTENSION_LIST).replace("extensions.", "") + "***"
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCog(bot))