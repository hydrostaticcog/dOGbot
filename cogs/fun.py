import discord

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog

class Fun(Cog):
    @commands.command(aliases=["p"])
    async def ping_pong(self, ctx: MyContext):
        """
        Play ping pong with dOGbot!
        """
        await ctx.message.delete()
        await ctx.send(":ping_pong:")

    @commands.command(aliases=["kuki"])
    async def cookie(self, ctx: MyContext):
        """
        Get a free cookie!
        """
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, here you go! :cookie:")

setup = Fun.setup