from discord.ext import commands

import json, asyncio, aiohttp, time, discord

description = """Terminal's Discord bot."""

startup_exts = ["moderation", "dice"]

prefixes = ["t!", "term!", "terminal "]

with open("./config.json", "r") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(*prefixes), description=description, owner_id=190544080164487168)

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


@bot.command(description="Loads an extension", aliases=["le"])
@commands.is_owner()
async def load(ctx, cog_name : str):
    """Loads an extension"""
    try:
        bot.load_extension("extensions."+cog_name)
        print("Loading extension {}".format(cog_name))
    except Exception as e:  # pylint: disable=bare-except
        await ctx.send("```\n{}```".format(e))
        return
    await ctx.send("Loaded extension {}".format(cog_name))
    

@bot.command(description="Unloads an extension", aliases=["ule"])
@commands.is_owner()
async def unload(ctx, ename : str):
    try:
        bot.unload_extension("extensions."+ename)
        print("Unloading extension {}".format(ename))
    except Exception as e:  # pylint: disable=bare-except
        await ctx.send("```\n{}```".format(e))
        return
    await ctx.send("Unloaded extension {}".format(ename))
    

if __name__ == "__main__": 
    for ext in startup_exts:
        try:
            print("Loading extension {}".format(ext))
            bot.load_extension(ext)
        except Exception as e:  # pylint: disable=bare-except
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load {}:\n{}".format(ext, exc))
    bot.run(config["token"])
