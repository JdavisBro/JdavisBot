import discord
from discord.ext import commands
import subprocess,time,requests,json

def setup(bot):
    bot.add_cog(minecraftServer(bot))

def minecraftCheck(ctx):
    return ctx.author.id == 105725338541101056 or ctx.author.id == 384774787823828995


class minecraftServer(commands.Cog):
    """Minecraft Server stuff for Jdavis' servers you can ignore this."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["mc"])
    @commands.check(minecraftCheck)
    async def minecraft(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    async def minecraftRun(self,cmd):
        subprocess.run(["screen","-S","minecraft","-X","stuff",'^M'])
        time.sleep(1)
        subprocess.run(["screen","-S","minecraft","-X","stuff",f'{cmd}^M'])

    @minecraft.command(name="run")
    async def minecraft_run(self,ctx,*,cmd):
        cmd = cmd.replace("^","")
        await self.minecraftRun(cmd)
        await ctx.send(f"Ran \"{cmd}\" command!")

    @minecraft.group(name="whitelist")
    async def minecraft_whitelist(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @minecraft_whitelist.command(name="remove")
    async def minecraft_whitelist_remove(self,ctx,name):
        await self.minecraftRun(f"whitelist remove {name}")
        await ctx.send(f"{name} removed from whitelist!")

    @minecraft_whitelist.group(name="add")
    async def minecraft_whitelist_add(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @minecraft_whitelist_add.command(name="java")
    async def minecraft_whitelist_add_java(self,ctx,name):
        await self.minecraftRun(f"whitelist add {name}")
        await ctx.send(f"{name} added to whitelist!")

    @minecraft_whitelist_add.command(name="bedrock")
    async def minecraft_whitelist_add_bedrock(self,ctx,*,name):
        uuid = requests.get(f"https://floodgate-uuid.heathmitchell1.repl.co/uuid?gamertag={name.replace(' ','+')}").text
        uuid = uuid[16+len(name):]
        name = ("*" if not name.startswith("*") else "")+name.replace(" ","_")
        whitelist = json.load(open("/home/jdavisbro221/minecraft/whitelist.json"))
        whitelist.append({"uuid":uuid,"name":name})
        with open("/home/jdavisbro221/minecraft/whitelist.json","w") as f:
            json.dump(whitelist,f)
        await self.minecraftRun("whitelist reload")
        await ctx.send(f"{name} with uuid {uuid} added to whitelist!")