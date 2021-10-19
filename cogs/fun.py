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
        await ctx.send(":ping_pong:")

    @commands.command(aliases=["kuki"])
    async def cookie(self, ctx: MyContext, recipient: discord.User = None):
        """
        Get/Give a free cookie!
        """
        if recipient:
            if recipient == ctx.author:
                await ctx.send(f"{recipient.mention}, You dont get a kuki you selfish brat!")
                return
            await ctx.send(f"{recipient.mention}, here is a <:Kuki:823597497997328416> from {ctx.author.mention}")
        else:
            await ctx.send(f"{ctx.author.mention}, here you go! <:Kuki:823597497997328416>")

setup = Fun.setup