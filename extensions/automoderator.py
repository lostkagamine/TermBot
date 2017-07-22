import discord, re
import rethinkdb as r
from discord.ext import commands

regex = "(?:discord(?:(?:\.|.?dot.?)gg|app(?:\.|.?dot.?)com\/invite)\/(([\w]{1,}|[abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789]{1,})))"


class AntiAdvertising():
            
    @commands.command()
    async def automodsetup(ctx, *args):
        print("ran")
        if args == None:
            return
        if args[0] == "invite":
            if args[1] == None:
                await ctx.send("Syntax: `automodsetup invite <ban/kick/delete>`")
                try:
                    t = r.db("termbot").table("automoderator_invites")
                except rethinkdb.errors.ReqlOpFailedError:
                    t = r.db("termbot").table_create("automoderator_invites")
                print(t)

    def __init__(self, bot):
        self.bot = bot
        self.conn = r.connect("localhost", 28015)
        @bot.listen("on_message")
        async def on_message(msg):
            if msg.guild.me.permissions_in(msg.channel).manage_messages == True:
                r = re.search(regex, msg.content)
                if r != None:
                    # handle stuff
                    try:
                        await msg.delete()
                        await msg.channel.send(":x: Do not advertise.")
                        await msg.author.kick(reason="Advertising (TermBot automoderator)")
                    except discord.Forbidden as e:
                        print(f"A user advertised, but I couldn't kick them because of permissions.\n{e}")


def setup(bot):
    bot.add_cog(AntiAdvertising(bot))
