import logging
import os
import sys
import time
import traceback

import discord
from discord.ext import commands

import storage

version = "0.0.0"

logging.basicConfig(format='[%(asctime)s] %(levelname)s - Bot: %(message)s', level=logging.INFO) 

try:
    TOKEN = sys.argv[1]
except:
    logging.info("Token not defined, must be the second argument (after filename) in the running command.")
    exit()

default_prefix = '-'

if not os.path.isdir('settings'):
    os.mkdir('settings')
    logging.info("Settings folder created.")

if storage.create('cogs',["cogs.owner.owner","cogs.custom.custom","cogs.mod.mod"])[0]:
    logging.info("settings/cogs.json created.")
if storage.create('prefixes',{})[0]:
    logging.info("settings/prefixes.json created.")

def prefix(bot, message):
    if isinstance(message.channel,discord.DMChannel):
        return commands.when_mentioned_or(f"{default_prefix} ",default_prefix)(bot,message)
    guildprefix = storage.read("prefixes",key=[str(message.guild.id)],default=default_prefix)
    prefixes = [f"{guildprefix} ",guildprefix]
    return commands.when_mentioned_or(*prefixes)(bot,message)

bot = commands.Bot(command_prefix=prefix, description=f'JdavisBot Version: {version}.', activity=discord.Game("Starting Up!"),case_insensitive=True)
bot.default_prefix = default_prefix
bot.startTime = time.time()
bot.currently_loaded_cogs = []
bot.version = version

extensions = storage.read("cogs")

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            logging.warning("{} was unable to be loaded.".format(extension))
            raise
        else:
            logging.info("{} loaded.".format(extension))
            bot.currently_loaded_cogs.append(extension.split(".")[2])

@bot.event
async def on_ready():
    logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logging.info(f'Discord.py Version: {discord.__version__}')
    await bot.change_presence(activity=discord.Game("with a Fox!"))

@bot.event
async def on_command_error(ctx, error):
    if ctx.command != None:
        if ctx.command.name == "raiseLastError":
            raise error
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"The argument {error.param} is missing!")
        await ctx.send_help(ctx.command)
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(error)
        return
    if isinstance(error, commands.CheckFailure):
        return
    await ctx.send(f"`{error} -- {ctx.command.name}`")
    await ctx.send_help(ctx.command)
    bot.lastError = error

@bot.command(name="oneTimeLoad",aliases = ["otl"])
@commands.is_owner()
async def base_oneTimeLoad(ctx,cog):
    """Loads cog for single time use"""
    try:
        bot.load_extension(f"cogs.{cog}.{cog}")
    except:
        await ctx.send("Unable to load that cog.")
    else:
        await ctx.send("Cog loaded!")

bot.run(TOKEN, bot=True, reconnect=True)
