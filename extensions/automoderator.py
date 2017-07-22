import discord, re, asyncio
import rethinkdb as r
from discord.ext import commands

regex = "(?:discord(?:(?:\.|.?dot.?)gg|app(?:\.|.?dot.?)com\/invite)\/(([\w]{1,}|[abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789]{1,})))"


class AntiAdvertising():
            
    @commands.command(pass_context=True)
    async def anti_ad_setup(self, ctx):
        if ctx.author.permissions_in(ctx.channel).manage_server == False:
            return
        if r.table("automoderator_invites").filter(r.row["guild"] == str(ctx.guild.id)).run(self.conn) != None:
            await ctx.send("This guild already has automoderation set up.")
            return
        m = await ctx.send("**TermBot Anti-Invite Feature**\n\nWhat punishment do you want advertisers to incur? (kick/ban/softban/delete/disable) [10 seconds]")
        def a(m):
            return (m.content == "ban" or m.content == "kick" or m.content == "delete" or m.content == "disable" or m.content == "softban") and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for("message", check=a, timeout=10)
        except asyncio.TimeoutError:
            await m.edit(content="Operation cancelled")
            return
        m.delete()
        r.table("automoderator_invites").insert({"guild": str(ctx.guild.id), "type": msg.content}).run(self.conn)
        await ctx.send("Set automoderation type to " + msg.content)



    def __init__(self, bot):
        self.bot = bot
        self.conn = r.connect("localhost", 28015, db="termbot")
        @bot.listen("on_message")
        async def on_message(msg):
            if msg.guild.me.permissions_in(msg.channel).manage_messages == True:
                reg = re.search(regex, msg.content)
                if reg != None:
                    # handle stuff
                    a = r.table("automoderator_invites").filter(r.row["guild"] == str(msg.guild.id)).run(self.conn).next()
                    if a != None:
                        
                        if a["type"] == "disable":
                            return
                        elif a["type"] == "kick":
                            await msg.delete()
                            try:
                                await msg.author.kick(reason="Advertising (TermBot Automoderator)")
                            except discord.Forbidden:
                                await msg.channel.send("I couldn't kick the user, have you tried giving me permissions to?")
                        elif a["type"] == "delete":
                            await msg.delete()
                        elif a["type"] == "softban":
                            await msg.delete()
                            try:
                                await msg.author.ban(reason="Advertising (TermBot Automoderator)", delete_message_days=7)
                                await msg.author.unban(reason="Advertising (TermBot Automoderator)")
                            except discord.Forbidden:
                                await msg.channel.send("I couldn't softban the user, have you tried giving me permissions to?")
                        elif a["type"] == "ban":
                            await msg.delete()
                            try:
                                await msg.author.ban(reason="Advertising (TermBot Automoderator)", delete_message_days=7)
                            except discord.Forbidden:
                                await msg.channel.send("I couldn't ban the user, have you tried giving me permissions to?")
                        
                        await msg.channel.send(":x: Do not advertise.")

                    


def setup(bot):
    bot.add_cog(AntiAdvertising(bot))
