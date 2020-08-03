import discord, asyncio
from discord.ext import commands
import random
import platform,os
import time, datetime, logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)        

def setup(bot):
    bot.add_cog(owner(bot))

class owner(commands.Cog):
    """owner cog!"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.previousReload = None
        self.database = bot.database

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
    async def load(self,ctx,*cogs):
        """Loads a cog."""
        await ctx.send("Are You Sure?!?\nIf you want to continue say `yes`.")
        def check(m):
            return m.content == 'yes' and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message',check=check,timeout=15)
        except asyncio.TimeoutError:
            await ctx.send("Timed Out. Not loading.")
        else:
            if msg.content == "yes":
                newloaded = []
                for cog in cogs:
                    if cog in self.bot.currently_loaded_cogs:
                        await ctx.send(f"{cog} already loaded.")
                        continue
                    try:
                        self.bot.load_extension("cogs.{0}.{0}".format(cog))
                    except:
                        await ctx.send(f"Failed to load {cog}")
                        raise
                    else:
                        self.bot.currently_loaded_cogs.append(cog)
                        newloaded.append((f"cogs.{cog}.{cog}",))
                        await ctx.send(f"Loaded {cog}")
                c = self.database.cursor()
                c.executemany("INSERT OR IGNORE INTO cogs VALUES (?)",newloaded)
                self.database.commit()
                await ctx.send(f"Done.")

    @cog.command(aliases = ['u'])
    async def unload(self,ctx,*cogs):
        """Unloads a cog."""
        newunloaded = []
        for cog in cogs:
            if cog == 'owner':
                await ctx.send("Not unloading owner.")
                continue
            try:
                self.bot.unload_extension("cogs.{0}.{0}".format(cog))
            except:
                await ctx.send(f"Failed to unload {cog}")
                raise
            else:
                if cog in self.bot.currently_loaded_cogs:
                    self.bot.currently_loaded_cogs.remove(cog)
                    newunloaded.append((f"cogs.{cog}.{cog}",))
                await ctx.send(f"Unloaded {cog}")
        c = self.database.cursor()
        c.executemany("DELETE FROM cogs WHERE cog=?",newunloaded)
        self.database.commit()
        await ctx.send(f"Done.")

    @cog.command(aliases = ['r'])
    async def reload(self,ctx,cog=None):
        """Reload cog."""
        if cog == None:
            if self.bot.previousReload == None:
                return
            else:
                cog = self.bot.previousReload
        try:
            self.bot.reload_extension("cogs.{0}.{0}".format(cog))
        except:
            await ctx.send("Failed.")
            raise
        else:
            await ctx.send("Cog {} reloaded.".format(cog))
            exec(f"self.bot.previousReload = cog")

    @cog.command(name="list",aliases=["ls"])
    async def cogs_list(self,ctx):
        """Lists loaded and unloaded cogs."""
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        unloaded_cogs = []
        for cog in filter(os.path.isdir, ["cogs/"+fileDir for fileDir in os.listdir("cogs")]):
            (unloaded_cogs.append(cog[5:])) if cog[5:] not in self.bot.currently_loaded_cogs else None
        embed = discord.Embed(colour=colour,title="Cogs.")
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Loaded Cogs:", value=", ".join(self.bot.currently_loaded_cogs)+".", inline=False)
        embed.add_field(name="Unloaded Cogs:", value=", ".join(unloaded_cogs)+".", inline=False)
        await ctx.send(embed=embed)

    @cog.command(aliases = ["otl"])
    async def oneTimeLoad(self,ctx,cog):
        """Loads cog for single time use"""
        try:
            self.bot.load_extension(f"cogs.{cog}.{cog}")
        except:
            await ctx.send("Unable to load that cog.")
        else:
            await ctx.send("Cog loaded!")
            self.bot.currently_loaded_cogs.append(cog)

    @cog.command(aliases = ["otul"])
    async def oneTimeUnload(self,ctx,cog):
        """Unloads cog for single time use"""
        try:
            self.bot.unload_extension(f"cogs.{cog}.{cog}")
        except:
            await ctx.send("Unable to unload that cog?")
        else:
            await ctx.send("Cog unloaded!")
            self.bot.currently_loaded_cogs.remove(cog)

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_alias(self,ctx,cog=None):
        command = self.bot.get_command("cog reload")
        await ctx.invoke(command,cog)

    @commands.command()
    async def info(self,ctx):
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        appinfo = await self.bot.application_info()
        embed = discord.Embed(colour=colour,description=":) JdavisBot!")
        embed.set_author(name="JdavisBot", url="https://wwww.github.com/JdavisBro/JdavisBot", icon_url=self.bot.user.avatar_url)
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

    @commands.command()
    @commands.is_owner()
    async def raiseLastError(self,ctx):
        raise self.bot.lastError

    @commands.command()
    @commands.is_owner()
    async def exec(self,ctx,*,executeThis):
        logging.info(f"Result: {exec(executeThis)}")
