import discord
import random
import time

from discord.ext import commands
from utils.ctx_class import MyContext
from utils.cog_class import Cog
from utils.models import get_from_db


class CookieCog(Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            ri = random.randint(1, 100)
            if ri >= 80:
                await self.give_cookies(message)
                await self.check_level(message)

    async def give_cookies(self, message):
        db_user = await get_from_db(message.author)
        cookies_tbg = random.randint(1, 5)
        self.bot.logger.debug(f"[LEVELING] - Gave {message.author} {cookies_tbg} cookies")
        db_user.cookies_avail = db_user.cookies_avail + cookies_tbg
        await db_user.save()

    async def check_level(self, message):
        db_user = await get_from_db(message.author)
        next_level = db_user.level + 1
        needed_to_advance = next_level * 20
        if db_user.cookies_avail >= needed_to_advance:
            db_user.cookie_jar += db_user.cookies_avail
            db_user.cookies_avail = 0
            db_user.level += 1
            await message.channel.send(
                f"{message.author.mention}, Congratulations! You have achieved level {next_level}"
                f"!\nYou currently have {db_user.cookie_jar} cookies.")
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
        if db_giv.cookie_jar - amount > 0:
            db_giv.cookie_jar -= amount
            db_recip.cookies_avail += amount
            await db_recip.save()
            await db_giv.save()
            await ctx.reply(f"Gave {recipient.mention} {amount} cookie(s)!")
            return
        if db_giv.cookie_jar - amount > 0:
            db_giv.cookies_avail -= amount
            db_recip.cookies_avail += amount
            await db_recip.save()
            await db_giv.save()
            await ctx.reply(f"Gave {recipient.mention} {amount} cookie(s)!")
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
        cookies = db_user.cookies_avail + db_user.cookie_jar
        level = f"{db_user.level}"
        nxl = db_user.level + 1
        progress = f"{db_user.cookies_avail}/{nxl * 20} to Level {nxl}"
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
            board.append([m.name, db.level, db.cookie_jar + db.cookies_avail])
        board.sort(reverse=True, key=self.sort_key2)
        embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="Top 10 users who have the most "
                                                                                   "cookies", color=self.bot.color)
        embed.add_field(name="First", value=board[0][0] + f" - Level {board[0][1]}", inline=False)
        embed.add_field(name="Second", value=board[1][0] + f" - Level {board[1][1]}", inline=False)
        embed.add_field(name="Third", value=board[2][0] + f" - Level {board[2][1]}", inline=False)
        embed.add_field(name="Fourth", value=board[3][0] + f" - Level {board[3][1]}", inline=False)
        embed.add_field(name="Fifth", value=board[4][0] + f" - Level {board[4][1]}", inline=False)
        embed.add_field(name="Sixth", value=board[5][0] + f" - Level {board[5][1]}", inline=False)
        embed.add_field(name="Seventh", value=board[6][0] + f" - Level {board[6][1]}", inline=False)
        embed.add_field(name="Eighth", value=board[7][0] + f" - Level {board[7][1]}", inline=False)
        embed.add_field(name="Ninth", value=board[8][0] + f" - Level {board[8][1]}", inline=False)
        embed.add_field(name="Tenth", value=board[9][0] + f" - Level {board[9][1]}", inline=False)
        await ctx.send(embed=embed)

    def sort_key2(self, company):
        return company[2]


setup = CookieCog.setup
