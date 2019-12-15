import discord
from discord.ext import commands
import logging,json,datetime

def setup(bot):
    bot.add_cog(economy(bot))

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO) 

try:
    open("cogs/economy/economy.json","x")
    json.dump(dict(),open("cogs/economy/economy.json","w"))
    logging.info("economy.json created.")
except:
    logging.info("economy.json found.")

try:
    open("settings/economy.json","x")
    json.dump({"starterMoney": "500","paydayMoney":"75","minimumGamblingCost": "10"},open("settings/economy.json","w"),indent=4)
    logging.info("settings/economy.json created.")
except:
    logging.info("settings/economy.json found.")

def getSetting(setting):
    with open("settings/economy.json","r+") as f:
        settings = json.load(f)
    return settings[setting]

def prefix(bot, message):
    with open("settings/prefixes.json","r+") as f:
        prefixes = json.load(f)
        return prefixes.get(str(message.guild.id), bot.default_prefix)

class economy(commands.Cog):
    """Economy cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def bank(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @bank.command(name="new",aliases=["create","setup"])
    async def bank_new(self,ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("cogs/economy/economy.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid in bankDict[guildid].keys():
            await ctx.send("You already have a bank account!")
            return
        bankDict[guildid][userid] = {"money": getSetting("starterMoney"),"nextPaydayTime": datetime.datetime.now().timestamp()}
        with open("cogs/economy/economy.json", "w+") as f:
            json.dump(bankDict,f)
        await ctx.send("Bank account created!")

    @bank.command(name="balance",aliases=["bal"])
    async def bank_balance(self,ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("cogs/economy/economy.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid not in bankDict[guildid]:
            await ctx.send(f"You don't have a bank account! You can create one with `{prefix(self.bot,ctx.message)}bank new`")
            return
        await ctx.send(f"You have £{bankDict[guildid][userid]['money']}!")

    @commands.command(name="balance",aliases=["bal"])
    async def balance_alias(self,ctx):
        command = self.bot.get_command("bank balance")
        await ctx.invoke(command)

    @commands.command(aliases=["pay","givemoney","paycheck","dollar"])
    async def payday(self,ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("cogs/economy/economy.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid not in bankDict[guildid].keys():
            await ctx.send(f"You don't have a bank account! You can create one with `{prefix(self.bot,ctx.message)}bank new`")
            return
        if int(bankDict[guildid][userid]["nextPaydayTime"]) < datetime.datetime.now().timestamp():
            pass
        else:
            timeLeft = datetime.datetime.fromtimestamp(float(bankDict[guildid][userid]['nextPaydayTime']) - datetime.datetime.now().timestamp())
            timeLeft = timeLeft.strftime("%M minutes and %S seconds")
            await ctx.send(f"You have to wait {timeLeft} until your next payday!")
            return
        bankDict[guildid][userid]["money"] = str(int(bankDict[guildid][userid]["money"])+int(getSetting("paydayMoney")))
        bankDict[guildid][userid]["nextPaydayTime"] = (datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()
        with open("cogs/economy/economy.json", "w+") as f:
            json.dump(bankDict,f)
        await ctx.send(f"£{getSetting('paydayMoney')} has been added to your account!")