import discord
import time
import json
import sys

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog

with open('release.json') as f:
    data = json.load(f)
    release = data['dgbVersion']
    rD = data['releaseDate']


class Utils(Cog):
    @commands.command()
    async def ping(self, ctx: MyContext):
        """
        Returns the latency of bot - Discord connection
        """
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        ping = str(time_delta) + "ms"
        latency = str(round(self.bot.latency * 1000)) + "ms"
        embed = discord.Embed(title=":ping_pong: dOGbot Ping!", color=discord.Color.orange())
        embed.add_field(name="API Ping", value=ping, inline=False)
        embed.add_field(name="WS Latency", value=latency)
        embed.set_footer(text=f"Current Bot Version: v{release}")
        await ctx.send(embed=embed)

    @commands.command()
    async def twitter(self, ctx: MyContext):
        """
        Check out dOGbone's Twitter!
        """
        await ctx.reply("<:Twitter:823582218332143666> Go check out dOGbone's Twitter! <https://twitter.com/dOGbon32>")

    @commands.command()
    async def youtube(self, ctx: MyContext):
        """
        Check out dOGbone's Youtube channel!
        """
        await ctx.reply(
            "<:Youtube:823582109959979028> Go check out dOGbone's Youtube channel! "
            "<https://www.youtube.com/channel/UCTDV8aurw0iQRjSBqw7aEEw>")

    @commands.command()
    async def twitch(self, ctx: MyContext):
        """
        Check out dOGbone's Twitch channel!
        """
        await ctx.reply(
            "<:Twitch:823582166231416884> Go check out dOGbone's Twitch channel! <https://www.twitch.tv/dogbon32>")

    @commands.command()
    async def version(self, ctx: MyContext):
        """
        Provides information about the current version of the bot, as well as a location to file formal bug
        reports/feature requests
        """
        embed = discord.Embed(title="dOGbot Version Information", color=discord.Color.orange())
        embed.add_field(name="Version", value=release, inline=True)
        embed.add_field(name="Release Date", value=rD, inline=True)
        embed.add_field(name="Have Issues or Features you want?",
                        value="Let us know on our GitHub page!\n<https://github.com/hydrostaticcog/dOGbot>",
                        inline=False)
        embed.add_field(name="System Information",
                        value=f'Running Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} on {sys.platform}')
        await ctx.send(embed=embed)

    @commands.command()
    async def credits(self, ctx: MyContext):
        """
        Credits developers of dOGbot
        """
        hydro: discord.User = await self.bot.fetch_user(711960088553717781)
        dog: discord.User = await self.bot.fetch_user(726866417588109314)
        ry: discord.User = await self.bot.fetch_user(712687059113869323)
        hydro_mention: str = hydro.mention
        dog_mention: str = dog.mention
        ry_mention: str = ry.mention
        embed = discord.Embed(title="dOGbot Credits", description="All the users that devoted time, resources, etc. to"
                                                                  " the development/growth of dOGbot",
                              color=discord.Color.orange())
        embed.add_field(name="Developer", value=hydro_mention)
        embed.add_field(name="Developed For", value=dog_mention)
        embed.add_field(name="Legacy Developer", value=ry_mention)
        embed.set_footer(text=f"Current Bot Version: v{release}")
        await ctx.send(embed=embed)


setup = Utils.setup
