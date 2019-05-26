import discord
from discord.ext import commands
import sys, traceback, logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)        
default_prefix = "-"
try:
    open("prefixes.txt","x")
    open("prefixes.txt","w").write("{}")
    logging.info("prefixes.txt created.")
except:
    logging.info("prefixes.txt found.")
try:
    open("cogs.txt","x")
    open("cogs.txt","w").write("[cogs.owner.owner]")
    logging.info("cogs.txt created.")
except:
    logging.info("cogs.txt found.")

def prefix(bot, message):
    with open("prefixes.txt") as f:
        prefixes = eval(f.read())
        return prefixes.get(message.guild.id, default_prefix)
bot = commands.Bot(command_prefix=prefix, description='Bruh.')

extensions = eval(open("cogs.txt","r").read())

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
        logging.info("{} loaded.".format(extension))

@bot.event
async def on_ready():
    logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logging.info(f'Version: {discord.__version__}')

bot.run(sys.argv[1], bot=True, reconnect=True)