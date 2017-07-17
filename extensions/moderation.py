import discord
import random
import asyncio
from discord.ext import commands

class Moderation():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Softban a user from your guild.")
    async def softban(self, ctx, member : discord.Member, *, reason : str = "[No reason specified]"):
        reason = f"[{str(ctx.author)}] {reason}"
        if ctx.author.guild_permissions.ban_members == False:
            await ctx.send("You do not have permissions.")
            return
        if ctx.me.guild_permissions.ban_members == False:
            await ctx.send("I don't have permission. Please give me Ban Members and try again.")
            return
        if member == ctx.guild.owner:
            await ctx.send("I can't do this.")
            return
        if member == ctx.me:
            await ctx.send("I can't do this.")
            return
        confcode = f"{random.randint(1000,9999)}"
        m = await ctx.send("""
        ```
        You want to softban the user {} for the reason of {}

        Please type in the code {} to confirm and softban this user, or wait 8 seconds to cancel.
        ```
        """.format(str(member), reason, confcode))
        def a(m):
            return m.content == confcode and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for("message", check=a, timeout=8)
        except asyncio.TimeoutError:
            await m.delete()
            await ctx.send("Operation cancelled.")
            return
        # print(str(msg))
        await m.delete()
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=7)
            await ctx.guild.unban(member, reason=reason, delete_message_days=7)
            await ctx.send("User {} was successfully softbanned.".format(str(member)))
        except (discord.HTTPException, discord.Forbidden) as e:
            await ctx.send("I couldn't softban the user. Have you checked I have the proper permissions and that my role is higher than the user you want to softban?")


    @commands.command(description="Kick a user from your guild.", aliases=["begone"])
    async def kick(self, ctx, member : discord.Member, *, reason : str = "[No reason specified]"):
        reason = f"[{str(ctx.author)}] {reason}"
        if ctx.author.guild_permissions.kick_members == False:
            await ctx.send("You do not have permissions.")
            return
        if ctx.me.guild_permissions.kick_members == False:
            await ctx.send("I don't have permission. Please give me Kick Members and try again.")
            return
        if member == ctx.guild.owner:
            await ctx.send("I can't do this.")
            return
        if member == ctx.me:
            await ctx.send("I can't do this.")
            return
        confcode = f"{random.randint(1000,9999)}"
        m = await ctx.send("""
        ```
        You want to kick the user {} for the reason of {}

        Please type in the code {} to confirm and kick this user, or wait 8 seconds to cancel.
        ```
        """.format(str(member), reason, confcode))
        def a(m):
            return m.content == confcode and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for("message", check=a, timeout=8)
        except asyncio.TimeoutError:
            await m.delete()
            await ctx.send("Operation cancelled.")
            return
        # print(str(msg))
        await m.delete()
        try:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send("User {} was successfully kicked.".format(str(member)))
        except (discord.HTTPException, discord.Forbidden) as e:
            await ctx.send("I couldn't kick the user. Have you checked I have the proper permissions and that my role is higher than the user you want to kick?")

    @commands.command(description="Ban a user from your guild.", aliases=["banne"])
    async def ban(self, ctx, member : discord.Member, *, reason : str = "[No reason specified]"):
        reason = f"[{str(ctx.author)}] {reason}"
        if ctx.author.guild_permissions.ban_members == False:
            await ctx.send("You do not have permissions.")
            return
        if ctx.me.guild_permissions.ban_members == False:
            await ctx.send("I don't have permission. Please give me Ban Members and try again.")
            return
        if member == ctx.guild.owner:
            await ctx.send("I can't do this.")
            return
        if member == ctx.me:
            await ctx.send("I can't do this.")
            return
        confcode = f"{random.randint(1000,9999)}"
        m = await ctx.send("""
        ```
        You want to ban the user {} for the reason of {}

        Please type in the code {} to confirm and ban this user, or wait 8 seconds to cancel.
        ```
        """.format(str(member), reason, confcode))
        def a(m):
            return m.content == confcode and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for("message", check=a, timeout=8)
        except asyncio.TimeoutError:
            await m.delete()
            await ctx.send("Operation cancelled.")
            return
        # print(str(msg))
        await m.delete()
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=7)
            await ctx.send("User {} was successfully banned.".format(str(member)))
        except (discord.HTTPException, discord.Forbidden) as e:
            await ctx.send("I couldn't ban the user. Have you checked I have the proper permissions and that my role is higher than the user you want to ban?")
            
        



def setup(bot):
    bot.add_cog(Moderation(bot))