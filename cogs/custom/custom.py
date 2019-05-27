import discord, asyncio, logging
from discord.ext import commands
import textwrap

def setup(bot):
    bot.add_cog(custom(bot))

try:
    open("cogs/custom/commands.txt","x")
    open("cogs/custom/commands.txt","w").write("{}")
    logging.info("commands.txt created.")
except:
    logging.info("commands.txt found.")

class custom(commands.Cog):
    """custom cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['cc','customcommand'])
    async def custom(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @custom.command(name='add')
    async def ccadd(self,ctx,name,*,content):
        if ctx.author.guild_permissions.manage_guild:
            f = open("cogs/custom/commands.txt")
            commands = eval(f.read())
            if ctx.guild.id not in commands:
                commands[ctx.guild.id] = '{}'
                f = open("cogs/custom/commands.txt","w")
                f.write(str(commands))
            if name in self.bot.commands:
                await ctx.send("There is already an actual command named that.")
            if name in commands[ctx.guild.id]:
                await ctx.send("Warning: There is already a command named {} in this server continuing would overwrite it.\nIf you want to continue say `yes`.".format(name))
                def check(m):
                    return m.content == 'yes' and m.channel == ctx.channel and m.author == ctx.author
                try:
                    msg = await self.bot.wait_for('message',check=check,timeout=15)
                except asyncio.TimeoutError:
                    await ctx.send("Timed Out. Not overwriting.")
                    return
                else:
                    if msg.content == "yes":
                        pass
            commands[ctx.guild.id][name] = content
            f = open("cogs/custom/commands.txt","w")
            f.write(str(commands))
            f.flush()
            await ctx.send("Command {} added!".format(name))

    @custom.command(name="del")
    async def ccdel(self,ctx,name):
        if ctx.author.guild_permissions.manage_guild:
            f = open("cogs/custom/commands.txt")
            commands = eval(f.read())
            if ctx.guild.id not in commands:
                commands[ctx.guild.id] = '{}'
                f = open("cogs/custom/commands.txt","w")
                f.write(str(commands))
                f.flush()
                await ctx.send("{} wasn't found.".format(name))
                return
            try:
                commands[ctx.guild.id].pop(name, None)
            except KeyError:
                await ctx.send("{} wasn't found.".format(name))
            except:
                raise
            else:
                f = open("cogs/custom/commands.txt","w")
                f.write(str(commands))
                f.flush()
                await ctx.send("Command {} deleted!".format(name))
            

    @custom.command()
    async def list(self,ctx):
        f = open("cogs/custom/commands.txt")
        commands = eval(f.read())
        if ctx.guild.id not in commands:
            commands[ctx.guild.id] = '{}'
            f = open("cogs/custom/commands.txt","w")
            f.write(str(commands))
            f.flush()
        if not commands[ctx.guild.id]:
            await ctx.send("There are no commands in this server.")
            return
        text = 'Custom Commands for {}:'.format(ctx.guild.name)
        for key in commands[ctx.guild.id]:
            text = '{}NEWLINE{}: {}'.format(text,str(key),str(commands[ctx.guild.id][key]))
        for line in textwrap.wrap(text, 1994):
            line = line.replace('NEWLINE','\n')
            await ctx.send("``{}``".format(line))
            await asyncio.sleep(1)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("settings/prefixes.txt") as f:
            prefixes = eval(f.read())
            prefix = prefixes.get(message.guild.id, '-')
        if message.content.startswith(prefix):
            f = open("cogs/custom/commands.txt")
            commands = eval(f.read())
            if message.guild.id not in commands:
                commands[message.guild.id] = '{}'
                return
            cmds=commands[message.guild.id]
            text = message.content.replace(prefix,'')
            strnumber=0
            txt=''
            args=''
            text=text.split()
            for word in text:
                if strnumber != 1:
                    strnumber = 1
                    txt = word
                else:
                    args += word
                    args += ' '
            length = len(args) - 1
            args = args[0:length]
            if txt not in cmds:
                return
            text = cmds[txt]
            text = text.replace("$A",args)
            await message.channel.send(text.format(message))
            