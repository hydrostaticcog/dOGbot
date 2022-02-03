import discord
import time
import json
import sys
import requests

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
        Returns the latency of bot -> Discord connection
        """
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        ping = str(time_delta) + "ms"
        latency = str(round(self.bot.latency * 1000)) + "ms"
        embed = discord.Embed(title=":ping_pong: dOGbot Ping!", color=self.bot.color)
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
        embed = discord.Embed(title="dOGbot Version Information", color=self.bot.color)
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
                              color=self.bot.color)
        embed.add_field(name="Developer", value=hydro_mention)
        embed.add_field(name="Developed For", value=dog_mention)
        embed.add_field(name="Legacy Developer", value=ry_mention)
        embed.set_footer(text=f"Current Bot Version: v{release}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["bug", "report"])
    async def bugs(self, ctx: MyContext):
        """
        Information on how to report bugs
        """
        version_info = f"{release} ({rD}) on Python{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} with platform {sys.platform}"
        embed = discord.Embed(title="Reporting bugs in dOGbot!", color=self.bot.color)
        embed.add_field(name="GitHub", value="Please report bugs to the developers at this bots GitHub Repository at "
                                             "this link: [Bug Form](https://github.com/hydrostaticcog/dOGbot/issues/new"
                                             "?assignees=hydrostaticcog&labels=bug&template=bug_report.md&title"
                                             "=%5BBUG%5D). Do not DM hydrostaticcog with bugs.", inline=False)
        embed.add_field(name="dOGbot version information", value=version_info, inline=False)
        await ctx.send(embed=embed)

    @commands.group()
    async def smp(self, ctx: MyContext):
        """
        Check out the Dog SMP!
        """
        if not ctx.invoked_subcommand:
            embed = discord.Embed(title="The Dog SMP!", color=self.bot.color, description="Join us on the Minecraft "
                                                                                          "Server!")
            embed.add_field(name="IP", value="`dog-smp.hydrostaticcog.me` Java/Bedrock (default ports)", inline=False)
            embed.add_field(name="Web Map", value="`https://dog-smp.hydrostaticcog.me:8123`")
            await ctx.send(embed=embed)

    @smp.command()
    async def ping(self, ctx: MyContext):
        """
        Checks the uptime of the SMP
        """
        resp = requests.get("https://api.mcsrvstat.us/2/dog-smp.hydrostaticcog.me")
        is_online = resp.json()['online']
        if is_online:
            status = "Online"
            emoji = ":green_circle:"
        else:
            status = "Offline"
            emoji = ":red_circle:"
        await ctx.send(f"{emoji} The Dog SMP is currently {status}")

    @commands.command(aliases=["reddit", "r/dogsmp"])
    async def subreddit(self, ctx: MyContext):
        """
        Provides information on the subreddit!
        """
        await ctx.send("<:Reddit:934847835462041651> Go check out the Dog SMP's subreddit! <https://dogsmp.reddit.com>")


setup = Utils.setup
