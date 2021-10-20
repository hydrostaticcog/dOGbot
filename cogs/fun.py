import discord
import random
import time

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog
from utils.models import get_from_db


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
            db_user = await get_from_db(recipient)
            db_user.cookies += 1
            await ctx.send(f"{recipient.mention}, here is a <:Kuki:823597497997328416> from {ctx.author.mention}")
            await db_user.save()
        else:
            db_user = await get_from_db(ctx.author)
            db_user.cookies += 1
            await ctx.reply("Here you go! <:Kuki:823597497997328416>")
            await db_user.save()

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx: MyContext, user: discord.Member = None):
        """
        Checks your/another user's inventory
        """
        if user is None:
            user = ctx.author
        db_user = await get_from_db(user)
        embed = discord.Embed(title=f"{user.name}'s Inventory", color=discord.Color.orange())
        embed.add_field(name="<:Kuki:823597497997328416> Cookies", value=db_user.cookies)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["flip", "coin", "h/t"])
    async def coin_flip(self, ctx: MyContext):
        """
        Flips a coin
        """
        result = "Tails"
        tf = random.randint(0, 1)
        if tf == 1:
            result = "Heads"
        await ctx.trigger_typing()
        m = await ctx.reply(":coin: Flipping the coin...")
        await m.edit(content=f":coin: {result}!")


setup = Fun.setup
