import discord
import random
import time

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog
from utils.models import get_from_db
from utils.embeds import leaderboard_embed


class CookieCog(Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            ri = random.randint(1, 100)
            if ri >= 75:
                await self.give_cookies(message)
                await self.check_level(message.author, message.channel)

    async def give_cookies(self, message):
        cookies_tbg = random.randint(1, 6)
        db_user = await get_from_db(message.author)
        og_cookies = db_user.cookies
        db_user.cookies = og_cookies + cookies_tbg
        await db_user.save()
        self.bot.logger.debug(f"[LEVELING] - Gave {message.author} {cookies_tbg} cookies. Had {og_cookies}, added {cookies_tbg}. Now has {db_user.cookies}")

    async def check_level(self, user, ctx):
        db_user = await get_from_db(user)
        next_level = db_user.level + 1
        needed_to_advance = db_user.last_level + next_level * 20
        if db_user.cookies >= needed_to_advance:
            db_user.level += 1
            db_user.last_level = needed_to_advance
            await ctx.send(
                f"{user.mention}, Congratulations! You have achieved level {next_level}"
                f"!\nYou currently have {db_user.cookies} cookies.")
            await db_user.save()
        elif db_user.cookies < db_user.last_level:
            db_user.level -= 1
            db_user.last_level -= db_user.level * 20
            await ctx.send(
                f"{user.mention}, Uh oh! You have lost a level! Your new level is {db_user.level}"
                f"!\nYou currently have {db_user.cookies} cookies.")
            await db_user.save()
        else:
            return

    @commands.command(aliases=["kuki"])
    async def cookie(self, ctx: MyContext, recipient: discord.Member, amount: int = 1):
        """
        Get/Give a cookie!
        """
        if recipient == ctx.author:
            await ctx.send(f"{recipient.mention}, You cannot give yourself cookies you silly goose!")
            return
        db_recip = await get_from_db(recipient)
        db_giv = await get_from_db(ctx.author)
        if db_giv.cookies - amount > 0:
            db_giv.cookies -= amount
            db_recip.cookies += amount
            await db_recip.save()
            await db_giv.save()
            await ctx.reply(f"Gave {recipient.mention} {amount} cookie(s)!")
            await self.check_level(ctx.author, ctx)
            await self.check_level(recipient, ctx)
            return
        else:
            await ctx.reply(f"You don't have enough cookies to give {recipient.mention} {amount} cookie(s)!")

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx: MyContext, user: discord.Member = None):
        """
        Checks your/another user's inventory
        """
        if user is None:
            user = ctx.author
        db_user = await get_from_db(user)
        cookies = db_user.cookies
        level = db_user.level
        nxl = db_user.level + 1
        nxl_thresh = nxl * 20
        progress = f"{cookies - db_user.last_level}/{nxl_thresh} to Level {nxl}"
        embed = discord.Embed(title=f"{user.name}'s Inventory", color=self.bot.color)
        embed.add_field(name="<:Kuki:823597497997328416> Cookies", value=cookies)
        embed.add_field(name="Level", value=level, inline=False)
        embed.add_field(name="Progress", value=progress, inline=False)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["lb", "leader"])
    async def leaderboard(self, ctx: MyContext):
        """
        Collects and displays the 10 users with the most cookies
        """
        board = []
        for m in ctx.guild.members:
            db = await get_from_db(m)
            if db.cookies > 0:
                board.append([m.name, db.level, db.cookies])
        board.sort(reverse=True, key=self.sort_key2)
        embed = await leaderboard_embed(ctx=ctx, bot=self.bot, board=board)
        await ctx.send(embed=embed)

    def sort_key2(self, company):
        return company[2]


setup = CookieCog.setup
