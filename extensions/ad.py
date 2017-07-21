import discord, re, rethinkdb
from discord.ext import commands

regex = "(?:discord(?:(?:\.|.?dot.?)gg|app(?:\.|.?dot.?)com\/invite)\/(([\w]{1,}|[abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789]{1,})))"


class AntiAdvertising():
    def __init__(self, bot):
        self.bot = bot
        @bot.event
        async def on_message(msg):
            print(msg.content)
            r = re.search(regex, msg.content)
            if r != None:
                # handle stuff
                msg.delete()
            
            bot.process_commands(msg) # IMPORTANT



def setup(bot):
    bot.add_cog(AntiAdvertising(bot))
