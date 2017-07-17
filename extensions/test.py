import discord
from discord.ext import commands

class TestExtension():
    def __init__(self, bot):
        self.bot = bot
    
    def setup(bot):
        bot.add_cog(TestExtension(bot))

    @self.bot.command()
    async def test(ctx):
        await ctx.send("Hi from a cog.")


def setup(bot):
    bot.add_cog(TestExtension(bot))