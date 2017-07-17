import discord
import random
import asyncio
from discord.ext import commands

class Moderation():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Ban a user from your guild.", aliases=["banne"])
    async def ban(self, ctx, member : discord.Member, *, reason : str = "[no reason specified]"):
        if ctx.author.guild_permissions.ban_members == False:
            await ctx.send("You do not have permissions.")
            return
        if ctx.me.guild_permissions.ban_members == False:
            await ctx.send("I don't have permission. Please give me Ban Members and try again.")
            return
        if member == ctx.guild.owner:
            await ctx.send("I can't do this.")
            return
        confcode = f"{random.randint(1000,9999)}"
        m = await ctx.send("""
        ```
        You want to ban the user {} for the reason of {}

        Please type in the code {} to confirm and ban this user, or wait 5 seconds to cancel.
        ```
        """.format(str(member), reason, confcode))
        def a(m):
            return m.content == confcode and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for("message", check=a, timeout=5)
        except asyncio.TimeoutError:
            await m.delete()
            await ctx.send("Operation cancelled.")
            return
        print(str(msg))
        await m.delete()
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=7)
            await ctx.send("User {} was successfully banned.".format(str(member)))
        except (HTTPException, Forbidden) as e:
            await ctx.send("I couldn't ban the user. Have you checked I have the proper permissions and that my role is higher than the user you want to ban's?")
            
        



def setup(bot):
    bot.add_cog(Moderation(bot))