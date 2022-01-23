import random

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog


class Fun(Cog):
    @commands.command(aliases=["p"])
    async def ping_pong(self, ctx: MyContext):
        """
        Play ping pong with dOGbot!
        """
        await ctx.send(":ping_pong:")

    @commands.command(aliases=["flip", "coin", "h/t"])
    async def coin_flip(self, ctx: MyContext):
        """
        Flips a coin
        """
        await ctx.trigger_typing()
        tf = bool(random.getrandbits(1))
        if tf:
            result = "Heads"
        else:
            result = "Tails"
        m = await ctx.reply(":coin: Flipping the coin...")
        await m.edit(content=f":coin: {result}!")


setup = Fun.setup
