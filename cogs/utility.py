import discord
import time

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog


class Utils(Cog):
    @commands.command()
    async def ping(self, ctx: MyContext):
        """
        Returns the latency of bot - Discord connection
        """
        await ctx.message.delete()
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        await ctx.send(f":ping_pong: Pong! Server response time: {time_delta}ms")

    @commands.command()
    async def twitter(self, ctx: MyContext):
        """
        Check out dOGbone's Twitter!
        """
        await ctx.send("<:Twitter:823582218332143666> Go check out dOGbone's Twitter! <https://twitter.com/dOGbon32>")

    @commands.command()
    async def youtube(self, ctx: MyContext):
        """
        Check out dOGbone's Youtube channel!
        """
        await ctx.send("<:Youtube:823582109959979028> Go check out dOGbone's Youtube channel! <https://www.youtube.com/channel/UCTDV8aurw0iQRjSBqw7aEEw>")

    @commands.command()
    async def twitch(self, ctx: MyContext):
        """
        Check out dOGbone's Twitch channel!
        """
        await ctx.send("<:Twitch:823582166231416884> Go check out dOGbone's Twitch channel! <https://www.twitch.tv/dogbon32>")




setup = Utils.setup