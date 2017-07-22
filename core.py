from discord.ext import commands

import json, asyncio, aiohttp, time, discord

import inspect # Eval
import re # Eval
import textwrap # Also Eval

with open("./config.json", "r") as f:
    config = json.load(f)

description = config["description"]

startup_exts = config["extensions"]["startup"]

prefixes = config["prefixes"]

bot_owners = config["owners"]

eval_env = {}

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(*prefixes), 
    description=description, 
    owner_id=190544080164487168, 
    game=discord.Game(name=config["game"]["name"], url=config["game"]["url"], type=config["game"]["status"]))

async def is_owner(ctx):
    return ctx.author.id in bot_owners

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
@commands.check(is_owner)
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
@commands.check(is_owner)
async def unload(ctx, ename : str):
    """Unloads an extension."""
    try:
        bot.unload_extension("extensions."+ename)
        print("Unloading extension {}".format(ename))
    except Exception as e:  # pylint: disable=bare-except
        await ctx.send("```\n{}```".format(e))
        return
    await ctx.send("Unloaded extension {}".format(ename))

@bot.command(description="Reloads an extension", aliases=["rle", "reloady"])
@commands.check(is_owner)
async def reload(ctx, ename : str):
    """Reloads an extension."""
    try:
        bot.unload_extension("extensions."+ename)
        print("Unloading extension {}".format(ename))
        bot.load_extension("extensions."+ename)
        print("Reloading extension {}".format(ename))
    except Exception as e: # pylint: disable=bare-except
        await ctx.send("```\n{}```".format(e))
        return
    await ctx.send("Reloaded extension {}".format(ename))

@bot.command(description="Stops the bot.", aliases=["quit", "disconnect", "stop"], name="exit")
@commands.check(is_owner)
async def _exit(ctx):
    await ctx.send("Bot shutting down...")
    exit()

@bot.command(description="Evaluates some code. VERY DANGEROUS.", aliases=["e", "ev"], name="eval")
@commands.check(is_owner)
async def _eval(ctx, *, code: str):
        env = {
            "message": ctx.message,
            "author": ctx.message.author,
            "channel": ctx.message.channel,
            "guild": ctx.message.guild,
            "ctx": ctx,
            "discord": discord,
            "bot": ctx.bot,
            "inspect": inspect
        }

        eval_env.update(env)

        code = code.strip("`")
        if code.startswith("py\n"):
            code = "\n".join(code.split("\n")[1:])
        if not re.search(
                r"^(return|import|for|while|def|class|from|[a-zA-Z0-9]+\s*=)",
                code, re.M) and len(code.split("\n")) == 1:
            code = "_ = "+code

        # Ignore this shitcode, it works
        _code = "\n".join([
            "async def func(bot, eval_env):",
            "    locals().update(eval_env)",
            "    old_locals = locals().copy()",
            "    try:",
            "{}",
            "        new_locals = {{k:v for k,v in locals().items() "
            "if k not in old_locals and k not in "
            "['old_locals','_','func']}}",
            "        if new_locals != {{}}:",
            "            return new_locals",
            "        else:",
            "            if '_' in locals() and inspect.isawaitable(_):",
            "                _ = await _",
            "            return _",
            "    finally:",
            "        eval_env.update({{k:v for k,v in locals().items() "
            "if k not in old_locals and k not in "
            "['old_locals','_','new_locals','func']}})"
        ]).format(textwrap.indent(code, '        '))

        exec(_code, eval_env)
        func = eval_env['func']
        res = await func(bot, eval_env)
        if res is not None:
            eval_env["_"] = res
            await ctx.send('```py\n{0}\n```'.format(res))
        else:
            await ctx.send("No additional output.")





if __name__ == "__main__": 
    for ext in startup_exts:
        try:
            print("Loading extension {}".format(ext))
            bot.load_extension("extensions."+ext)
        except Exception as e:  # pylint: disable=bare-except
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load {}:\n{}".format(ext, exc))
    bot.run(config["token"])
