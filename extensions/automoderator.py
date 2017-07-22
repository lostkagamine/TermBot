import discord, re, asyncio
import rethinkdb as r
from discord.ext import commands

regex = "(?:discord(?:(?:\.|.?dot.?)gg|app(?:\.|.?dot.?)com\/invite)\/(([\w]{1,}|[abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789]{1,})))"


class AntiAdvertising():
            
    @commands.command(pass_context=True)
    async def anti_ad_setup(self, ctx):
        m = await ctx.send("**TermBot Anti-Invite Feature**\n\nWhat punishment do you want advertisers to incur? (kick/ban/delete) [10 seconds]")
        def a(m):
            return (m.content == "ban" or m.content == "kick" or m.content == "delete") and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for("message", check=a, timeout=10)
        except asyncio.TimeoutError:
            await m.edit(content="Operation cancelled")
            return
        m.delete()
        r.db("termbot").table("automoderator_invites").insert({"guild": ctx.guild.id, "type": msg.content}).run(self.conn)
        await ctx.send("Set automoderation type to " + msg.content)



    def __init__(self, bot):
        self.bot = bot
        self.conn = r.connect("localhost", 28015)
        @bot.listen("on_message")
        async def on_message(msg):
            if msg.guild.me.permissions_in(msg.channel).manage_messages == True:
                r = re.search(regex, msg.content)
                if r != None:
                    # handle stuff
                    await msg.delete()

                    


def setup(bot):
    bot.add_cog(AntiAdvertising(bot))
