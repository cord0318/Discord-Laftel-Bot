import discord, asyncio
from discord.ext import commands
import config, importlib
import laftel

class LaftelCog(commands.Cog):
    def __init__(self, bot):
        importlib.reload(config)
        self.bot = bot
    
    @commands.command(name="laftel", aliases=["라프텔"])
    async def animation(self, ctx: commands.Context, *, name=None) -> None:
        if name != None:
            try:
                num_list = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
                data = await laftel.searchAnime(name)
                if len(data)==0: await ctx.send(embed=discord.Embed(title="[ LAFTEL ERROR ]", color=discord.Color.red(), description=f"**{name}**에 맞는 작품을 찾지 못했습니다."))
                else:
                    search_embed = discord.Embed(title="[ LAFTEL SEARCH ]", color=discord.Color.dark_blue(), description="원하시는 작품 번호를 선택하여 주세요.")
                    for results in data[:10]:
                        search_embed.add_field(name=f"{data.index(results)}번", value=results.name)
                    search_embed.set_footer(text="60초후에 종료됩니다.")
                    msg = await ctx.send(embed=search_embed)
                    for i in range(int(data.index(results) + 1)):
                        await msg.add_reaction(num_list[i])
                    def check(reaction, user):
                        return str(reaction) in ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"] and user == ctx.author and reaction.message.id == msg.id
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
                    int_var = num_list.index(str(reaction))
                    if ctx.author == user:
                        data = await laftel.getAnimeInfo(data[int_var].id)
                        embed = discord.Embed(color=discord.Color.dark_blue(), description="**[{} ({})](<{}>)**".format(data.name, data.id, data.url))
                        embed.set_thumbnail(url=data.image)
                        embed.add_field(name="Content", value=data.content.replace("\r\n", "")[:500], inline=False)
                        embed.add_field(name="Content Rating", value=data.content_rating)
                        if data.adultonly: adult = ":white_check_mark: 청불"
                        else: adult = ":x: 청불이 아님"
                        embed.add_field(name="Adult", value=adult)
                        if data.viewable: view = ":white_check_mark: 볼수 있음"
                        else: view = ":x: 볼수 없음"
                        embed.add_field(name="ViewAble", value=view)
                        embed.add_field(name="Genres", value=", ".join(data.genres))
                        embed.add_field(name="Tags", value=", ".join(data.tags))
                        embed.add_field(name="Airing Quarter", value=data.air_year_quarter)
                        if data.air_day==None: day = "없음"
                        else: day=data.air_day
                        embed.add_field(name="Airing Day", value=day)
                        embed.add_field(name="Rating", value=data.avg_rating)
                        embed.add_field(name="View Male/Female", value=f"{data.view_male} / {data.view_female}")
                        await msg.delete()
                        msg = await ctx.send(embed=embed) # send
            except asyncio.TimeoutError:
                await msg.edit(embed=discord.Embed(title="TIME OUT", description="시간이 종료되었습니다.", color=discord.Color.red()))
            except Exception as e:
                print("Laftel Error" + e)
            
        else:
            await ctx.send(f"<@!{ctx.author.id}> 작품 이름을 적어주세요.")


def setup(bot):
    bot.add_cog(LaftelCog(bot))