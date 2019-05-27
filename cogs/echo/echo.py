import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(echo(bot))

class echo(commands.Cog):
    """Echo cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self,ctx,*,echo):
        """Echos what you say"""
        try:
            await ctx.send(echo.format(ctx))
        except:
            await ctx.send("There was an error.")
