import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(admin(bot))

class admin(commands.Cog):
    """Admin cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def role(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @role.command(name = 'add')
    async def role_add(self,ctx,role: discord.Role,user: discord.Member = ''):
        if user == '':
            user = ctx.author
        await user.add_roles(role)
        await ctx.send("{} has been given the {} role.".format(user,role))
    
    @role.command(name = 'remove')
    async def role_remove(self,ctx,role: discord.Role,user: discord.Member = ''):
        if user == '':
            user = ctx.author
        await user.remove_roles(role)
        await ctx.send("{} has been removed from the {} role".format(user,role))