import discord
from discord.ext import commands


class TestExtension():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Hi from a cog.")

    @commands.command()
    async def test2(self, ctx):
        await ctx.send("Hi number 2.")


def setup(bot):
    bot.add_cog(TestExtension(bot))
