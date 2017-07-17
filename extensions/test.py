import discord
from discord.ext import commands


class TestExtension():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Hi from a cog.")


def setup(bot):
    bot.add_cog(TestExtension(bot))
