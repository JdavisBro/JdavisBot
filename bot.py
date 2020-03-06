import discord
from discord.ext import commands
import sys, traceback, logging
import time, os, json

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)        
default_prefix = '-'
if not os.path.isdir('settings'):
    os.mkdir('settings')
    logging.info("Settings folder created.")
def checkSettings(filename,write):
    try:
        open(f"settings/{filename}.json","x")
        json.dump(write,open(f"settings/{filename}.json","w"))
        logging.info(f"{filename}.json created.")
    except:
        logging.info(f"{filename}.json found.")

checkSettings('cogs',["cogs.owner.owner","cogs.custom.custom","cogs.mod.mod"])
checkSettings('prefixes',dict())

def prefix(bot, message):
    with open("settings/prefixes.json","r+") as f:
        prefixes = json.load(f)
        return prefixes.get(str(message.guild.id), default_prefix)

bot = commands.Bot(command_prefix=prefix, description='Bark Bark.', activity=discord.Game("Starting Up!"))
bot.default_prefix = default_prefix
bot.startTime = time.time()

with open("settings/cogs.json","r+") as f:
    extensions = json.load(f)

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            logging.warning("{} was unable to be loaded.".format(extension))
            raise
        else:
            logging.info("{} loaded.".format(extension))

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
        return
    await ctx.send(f"`{error} occured while running {ctx.command.name}`")
    bot.lastError = error

@bot.command(name="oneTimeLoad",aliases = ["otl"])
async def base_oneTimeLoad(ctx,cog):
    """Loads cog for single time use"""
    try:
        bot.load_extension(f"cogs.{cog}.{cog}")
    except:
        await ctx.send("Unable to load that cog.")
    else:
        await ctx.send("Cog loaded!")

bot.run(sys.argv[1], bot=True, reconnect=True)