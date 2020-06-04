import discord
from discord.ext import commands
import random,logging

def setup(bot):
    bot.add_cog(fun(bot))

class fun(commands.Cog):
    """Fun cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="fun",aliases=["f"])
    async def grp_fun(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @grp_fun.command(name="coolness",aliases=["cool"])
    async def grp_fun_coolness(self,ctx,*,user:discord.Member=None):
        if not user:
            user = ctx.author
        if user != ctx.guild.me:
            random.seed(user.id)
            if user.bot:
                if random.random() != 0:
                    await ctx.send(f"{user.display_name} is {round(random.random()*100/2,2)}% cool! (half as cool as usual because they're a bot)")
                else:
                    await ctx.send(f"{user.display_name} is {round(random.random()*100,2)}% cool! (half as cool as usual because they are a bot)")
            else:
                await ctx.send(f"{user.display_name} is {round(random.random()*100,2)}% cool!")
            random.seed()
        else:
            await ctx.send("I am 100% cool")