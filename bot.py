import discord
from discord.ext import commands
import sys, traceback, logging
import time

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)        
default_prefix = '-'
def checkSettings(filename,write):
    try:
        open("settings/{}.txt".format(filename),"x")
        open("settings/{}.txt".format(filename),"w").write(write)
        logging.info("{}.txt created.".format(filename))
    except:
        logging.info("{}.txt found.".format(filename))
checkSettings('cogs',"['cogs.owner.owner','cogs.custom.custom','cogs.mod.mod']")
checkSettings('prefixes','{}')
def prefix(bot, message):
    with open("settings/prefixes.txt") as f:
        prefixes = eval(f.read())
        return prefixes.get(message.guild.id, default_prefix)
bot = commands.Bot(command_prefix=prefix, description='Bruh.')
bot.default_prefix = default_prefix
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
        return
    await ctx.send("`{} occured while running {}`".format(error,ctx.command.name))
    await ctx.send_help(ctx.command)
    raise error

bot.run(sys.argv[1], bot=True, reconnect=True)