import discord, asyncio
from discord.ext import commands
import random
import platform
import time, datetime

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

    @commands.group(aliases = ['c'])
    @commands.is_owner()
    async def cog(self,ctx):
        """Commands to add, reload and remove cogs."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cog.command(aliases = ['l'])
    async def load(self,ctx,cog):
        """Loads a cog."""
        await ctx.send("Warning: If you installed this cog from online it could damage your BruhBot installation.\nIf you want to continue say `yes`.")
        def check(m):
            return m.content == 'yes' and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message',check=check,timeout=15)
        except asyncio.TimeoutError:
            await ctx.send("Timed Out. Not loading.")
        else:
            if msg.content == "yes":
                try:
                    self.bot.load_extension("cogs.{0}.{0}".format(cog))
                except:
                    await ctx.send("Failed.")
                    raise
                else:
                    extensions = eval(open("settings/cogs.txt","r").read())
                    extensions.append("cogs.{0}.{0}".format(cog))
                    f=open("settings/cogs.txt","w")
                    f.write(str(extensions))
                    f.flush
                    await ctx.send("Cog {} loaded.".format(cog))

    @cog.command(aliases = ['u'])
    async def unload(self,ctx,cog):
        """Unloads a cog."""
        if cog == 'owner':
            await ctx.send("Bruh, unloading owner would make you unable to load cogs, so that's a no.")
            return
        try:
            self.bot.unload_extension("cogs.{0}.{0}".format(cog))
        except:
            await ctx.send("Failed.")
            raise
        else:
            extensions = eval(open("settings/cogs.txt","r").read())
            extensions.remove("cogs.{0}.{0}".format(cog))
            f=open("settings/cogs.txt","w")
            f.write(str(extensions))
            f.flush
            await ctx.send("Cog {} removed.".format(cog))

    @cog.command(aliases = ['r'])
    async def reload(self,ctx,cog):
        """Reload cog."""
        try:
            self.bot.reload_extension("cogs.{0}.{0}".format(cog))
        except:
            await ctx.send("Failed.")
            raise
        else:
            await ctx.send("Cog {} reloaded.".format(cog))

    @commands.command()
    async def info(self,ctx):
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        appinfo = await self.bot.application_info()
        embed = discord.Embed(colour=colour)
        embed.set_author(name="BruhBot", url="https://wwww.github.com/JdavisBro/bruhbot", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Instance Owner:", value=appinfo.owner, inline=True)
        embed.add_field(name="Python Version:", value="[{}](https://www.python.org)".format(platform.python_version()), inline=True)
        embed.add_field(name="Discord.py Version:", value="[{}](https://github.com/Rapptz/discord.py)".format(discord.__version__), inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self,ctx):
        'Shows you how long the bot has been online'
        currentTime = time.time()
        uptime = int(round(currentTime - self.bot.startTime))
        uptime = str(datetime.timedelta(seconds=uptime))
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        embed = discord.Embed(title="I have been up for", description=uptime, color=colour)
        await ctx.send(embed=embed)

