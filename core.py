from discord.ext import commands

import json, asyncio, aiohttp, time

description = """Terminal's Discord bot."""

startup_cogs = ["moderation", "dice"]

prefixes = ["t!", "term!", "terminal "]

with open("./config.json", "r") as f:
    config = json.load(f)

async def getPrefix(bot, message):
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=getPrefix, description=description, owner_id=[190544080164487168, 161866631004422144, 86477779717066752])

@bot.event
async def on_ready():
    print("Bot logged in successfully: {} ({})".format(bot.user.name, bot.user.id))

@bot.command(description="Pong!")
async def ping(ctx):
    """Pong!"""
    before = time.monotonic()
    pong = await ctx.send("...")
    after = time.monotonic()
    ping = (after - before) * 1000
    await pong.edit(content="Pong! {}ms".format(int(ping)))

bot.run(config["token"])