import discord
import time
from profanity import profanity
from datetime import datetime

from discord.ext import commands

from utils.ctx_class import MyContext
from utils.cog_class import Cog
from utils.models import get_from_db_act, get_from_db_dobj
from utils.embeds import mod_message_embed


async def check_warns(member: discord.Member):
    db = await get_from_db_dobj(member)
    if db.warns > 3:
        await member.ban(reason="More than 3 warnings!")
    return


async def create_case(victim: discord.Member, issuer: discord.User, reason, guild: discord.Guild, type):
    case_id = round(time.time())
    db = await get_from_db_act(case_id)
    db.issuer_id = issuer.id
    db.victim_id = victim.id
    db.note = reason
    db.type = type
    db.guild_id = guild.id
    await db.save()
    return case_id


class ModCog(Cog):
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: MyContext, user: discord.Member, *, reason: str = "none given"):
        """
        Ban a user
        """
        case_id = await create_case(user, ctx.author, reason, ctx.guild, "ban")
        await ctx.guild.ban(user, reason=reason)
        await mod_message_embed(ctx, self.bot, case_id, "ban", reason)
        await ctx.send(f":ok_hand: - Banned {user.mention}, case ID {case_id}")

    @commands.command()
    @commands.has_permissions(manage_members=True)
    async def case(self, ctx: MyContext, id):
        """
        Get a case/mod action
        """
        db = await get_from_db_act(id)
        if ctx.guild.id != db.guild_id:
            if not await self.bot.is_owner(ctx.author):
                return await ctx.send("You do not have permission to view this action as it is from a different guild!")
        victim = await self.bot.fetch_user(db.victim_id)
        issuer = await self.bot.fetch_user(db.issuer_id)
        ts = datetime.fromtimestamp(db.id)
        embed = discord.Embed(title=f"Case #{id}", description=f"Type: {db.type}", color=self.bot.color)
        embed.add_field(name="Victim", value=victim.mention, inline=False)
        embed.add_field(name="Reason", value=db.note, inline=False)
        embed.add_field(name="Issuer", value=issuer.mention, inline=False)
        embed.add_field(name="Timestamp", value=str(ts), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: MyContext, user: discord.Member, *, reason: str = "none given"):
        """
        Kick a user
        """
        case_id = await create_case(user, ctx.author, reason, ctx.guild, "kick")
        await ctx.guild.kick(user)
        await ctx.send(f":ok_hand: - Kicked {user.mention}, case ID {case_id}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if profanity.contains_profanity(message.content):
            await message.delete()
            db = await get_from_db_dobj(message.author)
            db.warns += 1
            await db.save()
            await check_warns(message.author)


setup = ModCog.setup