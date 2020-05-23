import discord
from discord.ext import commands
import logging,json,datetime,random

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

    @bank.group(name="mod")
    @commands.has_permissions(manage_guild=True)
    async def bank_mod(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @bank_mod.command(name="set")
    async def bank_mod_set(self,ctx,user:discord.Member,money:int):
        guildid = str(ctx.guild.id)
        userid = str(user.id)
        with open("cogs/economy/economy.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid not in bankDict[guildid].keys():
            await ctx.send(f"That user doesn't have a bank account! They can create one with `{prefix(self.bot,ctx.message)}bank new`")
            return
        bankDict[guildid][userid]["money"] = money
        with open("cogs/economy/economy.json", "w+") as f:
            json.dump(bankDict,f)
        username = user.display_name + "'" if user.display_name.endswith('s') else user.display_name + "'s"
        await ctx.send(f"{username} account has been set to £{money}!")

    @bank_mod.command(name="paydayNow")
    async def bank_mod_paydaynow(self,ctx,user:discord.Member=None):
        if not user:
            user = ctx.author
        guildid = str(ctx.guild.id)
        userid = str(user.id)
        with open("cogs/economy/economy.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid not in bankDict[guildid].keys():
            await ctx.send(f"That user doesn't have a bank account! They can create one with `{prefix(self.bot,ctx.message)}bank new`")
            return
        bankDict[guildid][userid]["nextPaydayTime"] = 0
        with open("cogs/economy/economy.json", "w+") as f:
            json.dump(bankDict,f)
        username = user.display_name + "'" if user.display_name.endswith('s') else user.display_name + "'s"
        await ctx.send(f"{username} payday timer has been set to 0!")

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

    @commands.command(name="gamble")
    async def economy_gamble(self,ctx,amount:int):
        if amount < int(getSetting("minimumGamblingCost")):
            await ctx.send(f"Your gamble has to be at least {getSetting('minimumGamblingCost')}.")
            return
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("cogs/economy/economy.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid not in bankDict[guildid].keys():
            await ctx.send(f"You don't have a bank account! You can create one with `{prefix(self.bot,ctx.message)}bank new`")
            return
        if int(bankDict[guildid][userid]["money"]) < amount:
            await ctx.send("Your balance is too low to gamble that much!")
            return
        if random.randint(0,1) == 0:
            moneyToAdd = amount * -1
            await ctx.send(f"You lost! You now have £{int(bankDict[guildid][userid]['money']) + moneyToAdd} now!")
        else:
            moneyToAdd = amount
            await ctx.send(f"You won! You now have £{int(bankDict[guildid][userid]['money'])+moneyToAdd} now!")
        bankDict[guildid][userid]["money"] = str(int(bankDict[guildid][userid]["money"]) + moneyToAdd)
        with open("cogs/economy/economy.json", "w+") as f:
            json.dump(bankDict,f)