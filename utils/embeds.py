import discord
from typing import List

from utils.bot_class import dOGbot
from utils.ctx_class import MyContext


async def leaderboard_embed(ctx: MyContext = None, bot: dOGbot = None, board: List = None):
    embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="Top 10 users who have the most "
                                                                               "cookies", color=bot.color)
    counter = 0
    while counter <= 10:
        try:
            embed.add_field(name=str(counter + 1), value=f"{board[counter][0]} - Level {board[counter][1]} "
                            f"- {board[counter][2]} Cookies",
                            inline=False)
        except IndexError:
            return embed
        counter += 1
    return embed
