import discord
from discord.ext import commands
import sys, traceback, logging
import time

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)        
default_prefix = "-"
try:
    open("settings/prefixes.txt","x")
    open("settings/prefixes.txt","w").write("{}")
    logging.info("prefixes.txt created.")
except:
    logging.info("prefixes.txt found.")
try:
    open("settings/cogs.txt","x")
    open("settings/cogs.txt","w").write("[cogs.owner.owner],[cogs.custom.custom]")
    logging.info("cogs.txt created.")
except:
    logging.info("cogs.txt found.")

def prefix(bot, message):
    with open("settings/prefixes.txt") as f:
        prefixes = eval(f.read())
        return prefixes.get(message.guild.id, default_prefix)
bot = commands.Bot(command_prefix=prefix, description='Bruh.')
bot.startTime = time.time()
extensions = eval(open("settings/cogs.txt","r").read())

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            logging.warning("{} was unable to be loaded.".format(extension))
        else:
            logging.info("{} loaded.".format(extension))

@bot.event
async def on_ready():
    logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logging.info(f'Version: {discord.__version__}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        channel = ctx.channel
        return
    raise error

bot.run(sys.argv[1], bot=True, reconnect=True)