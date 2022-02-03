import discord
from typing import List

from utils.bot_class import dOGbot
from utils.ctx_class import MyContext


async def leaderboard_embed(ctx: MyContext = None, bot: dOGbot = None, board: List = None):
    embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="Top 10 users who have the most "
                                                                               "cookies", color=bot.color)
    for (idx, item) in enumerate(board):
        if idx == 10:
            break
        embed.add_field(name=str(idx + 1), value=f"{item[0]} - Level {item[1]} "
                                                 f"- {item[2]} Cookies",
                        inline=False)
    return embed


async def mod_message_embed(ctx: MyContext = None, bot: dOGbot = None, case_id=0, type="not specified",
                            reason="not given"):
    embed = discord.Embed(title="New Action on You", description=f"Type: {type}\nGuild: {ctx.guild.name}\nCase ID: {case_id}",
                          color=bot.color)
    embed.add_field(name="Reason", value=reason, inline=False)
    if type == "ban":
        embed.add_field(name="Appeals", value="Please contact the moderator of your choice to appeal this",
                        inline=False)
    return embed
