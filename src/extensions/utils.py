import discord, datetime
from discord.ext import commands

class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="userinfo", aliases=["유저정보", "user", "유저", "pf", "profile"])
    async def userinfo(self, ctx: commands.Context, user:discord.Member=None):
        if not user:
            user = ctx.author
        now = datetime.datetime.now()
        embed = discord.Embed(color=0x352E2D, title=f"{user}님의 정보")
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Name", value=f"{user}")
        embed.add_field(name="ID", value=f"{user.id}")
        if user.bot:
            plus_text = f":white_check_mark: 봇입니다."
        else: 
            plus_text = f":x: 봇이 아닙니다."
        if user.activity == None: act = "없음"
        else: act = user.activity.name
        if user.top_role.mention == None: top_role = "없음"
        else: top_role = user.top_role.mention
        if user.status == None: status = "없음"
        else: status = user.status
        embed.add_field(name="Bot", value=plus_text)
        embed.add_field(name="Activity", value=f"{act}")
        embed.add_field(name="Top Role", value=f"{top_role}")
        embed.add_field(name="Status", value=f"{status}")
        embed.add_field(name="Created at", value=user.created_at.strftime("%Y/%m/%#d %I:%M"))
        embed.add_field(name="Joined at", value=user.joined_at.strftime("%Y/%m/%#d %I:%M"))
        embed.set_footer(text="{} • {}".format(ctx.author, now.strftime("%Y·%m·%#d")), icon_url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="profile_picture", aliases=["프사", "프로필사진"])
    async def profile_picture(self, ctx: commands.Context, user:discord.Member=None):
        if not user: user = ctx.author
        embed = discord.Embed(title=user, description=f"**[사진 다운받기](<{user.avatar_url}>)**")  
        embed.set_image(url=str(user.avatar_url))
        await ctx.send(embed=embed)
    
    @commands.command(name="ping", aliases=["핑"])
    async def ping(self, ctx: commands.Context):
        text = ""
        if ctx.channel.type != discord.ChannelType.private:
            text += f"`이 서버의 Shard ID: {ctx.guild.shard_id}`\n"
        text += "```"
        for shard in self.bot.shards.values():
            text += f"Shard#{shard.id}: {int(shard.latency*1000)}ms\n"
        text += "```"
        embed = discord.Embed(title="Pong! :ping_pong: ", description=text, color=discord.Color.red())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UtilCog(bot))