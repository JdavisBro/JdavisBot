import discord
from discord.ext import commands
import logging,json

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

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self,ctx,time:int,name,*,items):
        """Creates a poll people can react to! Seperate items with ;"""
        channelid = str(ctx.channel.id)
        with open("cogs/poll/polls.json", "r+") as f:
            polls = json.load(f)
        if channelid in polls:
            await ctx.send("There's already a poll going on in this channel")
        items = items.split(";")
        if len(items) > 9:
            await ctx.send("The max amount of items is 9.")
            return
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