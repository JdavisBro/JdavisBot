import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(owner(bot))

class owner(commands.Cog):
    """owner cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        await ctx.send("👋 Goodbye")
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def run(self,ctx,*,command):
        try:
            exec(command)
        except:
            return
        await ctx.message.add_reaction("✅")

    @commands.group()
    @commands.is_owner()
    async def cog(self,ctx):
        """Commands to add, reload and remove cogs."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cog.command()
    async def load(self,ctx,cog):
        """Loads a cog."""
        try:
            self.bot.load_extension("cogs.{0}.{0}".format(cog))
        except:
            await ctx.send("Failed.")
            return
        else:
            extensions.append("cogs.{0}.{0}".format(cog))
            f=open("cogs.txt","w")
            f.write(str(extensions))
            f.flush
            await ctx.send("Cog {} loaded.".format(cog))

    @cog.command()
    async def unload(self,ctx,cog):
        """Unloads a cog."""
        if cog == 'owner':
            await ctx.send("Bruh, unloading owner would make you unable to load cogs, so that's a no.")
            return
        try:
            self.bot.unload_extension("cogs.{0}.{0}".format(cog))
        except:
            await ctx.send("Failed.")
            return
        else:
            extensions.remove("cogs.{0}.{0}".format(cog))
            f=open("cogs.txt","w")
            f.write(str(extensions))
            f.flush
            await ctx.send("Cog {} removed.".format(cog))

    @cog.command()
    async def reload(self,ctx,cog):
        """Reload cog."""
        try:
            self.bot.reload_extension("cogs.{0}.{0}".format(cog))
        except:
            await ctx.send("Failed.")
            return
        else:
            await ctx.send("Cog {} reloaded.".format(cog))

