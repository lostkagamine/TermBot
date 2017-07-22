import discord, re, asyncio, json
import rethinkdb as r
from discord.ext import commands

regex = "(?:discord(?:(?:\.|.?dot.?)gg|app(?:\.|.?dot.?)com\/invite)\/(([\w]{1,}|[abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789]{1,})))"


class AntiAdvertising():
            
    @commands.command(pass_context=True, aliases=["aas"])
    async def anti_ad_setup(self, ctx):
        if ctx.author.permissions_in(ctx.channel).manage_guild == False:
            await ctx.send("You must have Manage Server to be able to use this.")
            return
        try:
            a = r.table("automoderator_invites").filter(r.row["guild"] == str(ctx.guild.id)).run(self.conn).next()
        except r.net.DefaultCursorEmpty:
            pass
        else:
            await ctx.send("Automoderation already set up")
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

    @commands.command(pass_context=True, aliases=["caa"])
    async def clear_anti_ad(self, ctx):
        if ctx.author.permissions_in(ctx.channel).manage_guild == False:
            await ctx.send("You must have Manage Server to be able to use this.")
            return
        a = r.table("automoderator_invites").filter(r.row["guild"] == str(ctx.guild.id)).delete().run(self.conn)
        if a["deleted"] == 0:
            await ctx.send("This server didn't have any anti-ad feature settings.")
        else:
            await ctx.send("Cleared anti-ad feature settings.")
        


    def __init__(self, bot):
        with open("./config.json", "r") as f:
            config = json.load(f)
        self.bot = bot
        self.conn = r.connect(config["rethinkdb"]["host"], config["rethinkdb"]["port"], db=config["rethinkdb"]["db"])
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
