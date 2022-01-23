from discord.ext import commands

from utils.bot_class import dOGbot


class Cog(commands.Cog):
    def __init__(self, bot: dOGbot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args, **kwargs)

    @classmethod
    def setup(cls, bot: dOGbot):
        return bot.add_cog(cls(bot))

    def config(self):
        config = self.bot.config
        cog_config = config["cogs"].get(self.qualified_name, {})
        return cog_config
