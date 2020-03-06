import discord
from discord.ext import commands
import logging,json,datetime,asyncio

def setup(bot):
    bot.add_cog(poll(bot))

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO) 

try:
    open("cogs/poll/polls.json","x")
    json.dump(dict(),open("cogs/poll/polls.json","w"))
    logging.info("polls.json created.")
except:
    logging.info("polls.json found.")

class poll(commands.Cog):
    """Poll cog!"""

    async def checkPolls(self):
        while True:
            with open("cogs/poll/polls.json", "r+") as f:
                polls = json.load(f)
            pollsToPop = []
            for channelid in polls.keys():
                if datetime.datetime.now().timestamp() > polls[channelid]["time"]:
                    await self.bot.get_channel(int(channelid)).send("Poll Over!")
                    pollsToPop.append(channelid)
            for poll in pollsToPop:
                polls.pop(channelid)
            with open("cogs/poll/polls.json","w+") as f:
                json.dump(polls,f)
            await asyncio.sleep(2)

    def __init__(self, bot):
            self.bot = bot
            self.bot.loop.create_task(poll.checkPolls(self))

    @commands.command()
    async def poll(self,ctx,time:int,name:str,*,items:str):
        """Creates a poll people can react to! Time in seconds, seperate items with ;"""
        channelid = str(ctx.channel.id)
        with open("cogs/poll/polls.json", "r+") as f:
            polls = json.load(f)
        if channelid in polls:
            await ctx.send("There's already a poll going on in this channel")
        items = items.split(";")
        if len(items) > 9:
            await ctx.send("The max amount of items is 9.")
            return
        if len(items) == 0:
            await ctx.send("At least have 1 item!")
        time = (datetime.datetime.now() + datetime.timedelta(seconds=time)).timestamp()
        polls[channelid] = {"time": time,"name": name,"items": items,"userID": str(ctx.author.id)}
        with open("cogs/poll/polls.json", "w+") as f:
            json.dump(polls,f)
        embed = discord.Embed(title=name)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        itemnumber = 1
        for item in items:
            embed.add_field(name=itemnumber, value=item, inline=True)
            itemnumber += 1
        await ctx.send(embed=embed)

    @commands.command()
    async def stopPoll(self,ctx):
        await ctx.send("LOL")