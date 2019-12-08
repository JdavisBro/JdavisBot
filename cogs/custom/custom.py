import discord, asyncio, logging
from discord.ext import commands
import textwrap, json

def setup(bot):
    bot.add_cog(custom(bot))

try:
    open("cogs/custom/commands.json","x")
    open("cogs/custom/commands.json","w").write("{}")
    logging.info("commands.json created.")
except:
    logging.info("commands.json found.")

class custom(commands.Cog):
    """Cog to add custom commands for servers!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['cc','customcommand'])
    async def custom(self,ctx):
        """Commands to add custom commands to each server."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @custom.command(name='add',aliases = ['new','make','a'])
    @commands.has_permissions(manage_guild=True)
    async def cc_add(self,ctx,name,*,content):
        """Adds a custom command for this server, requires manage server permissions.
        You can use arguments to the context class if you do
        {.messagearguments}. For example .guild.name .channel.id .author.display_name .
        if you want to use more than one ctx argument you add a 0, e.g {0.message.id}
        you can also add arguments that the user fills in with $A"""
        with open("cogs/custom/commands.json", "r+") as f:
            commandServerDict = json.load(f)
        if ctx.guild.id not in commandServerDict:
            commandServerDict[ctx.guild.id] = dict()
            with open("cogs/custom/commands.json", "r+") as f:
                json.dump(commandServerDict,f)
        if name in self.bot.commands:
            await ctx.send("There is already an actual command named that.")
            return
        if name in commandServerDict[ctx.guild.id]:
            await ctx.send("Warning: There is already a command named '{}' in this server continuing would overwrite it.\nIf you want to continue say `yes`.".format(name))
            def check(m):
                return m.content == 'yes' and m.channel == ctx.channel and m.author == ctx.author
            try:
                msg = await self.bot.wait_for('message',check=check,timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("Timed Out. Not overwriting.")
                return
            else:
                if msg.content == "yes":
                    await ctx.send("Overwriting.")
        commandServerDict[ctx.guild.id][name] = content
        with open("cogs/custom/commands.json","r+") as f:
            json.dump(commandServerDict,f)
        await ctx.send("Command {} added!".format(name))

    @custom.command(name="del", aliases = ['delete','remove','d'])
    @commands.has_permissions(manage_guild=True)
    async def cc_del(self,ctx,name):
        """Deltes a custom command for this server, requires manage server permission."""
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
        
    @custom.command(name = 'list',aliases = ['get','view','l','ls'])
    async def cc_list(self,ctx):
        """Lists custom commands for this server."""
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
            text = '{}NEWLINE{}: {}'.format(text,str(key),commands[ctx.guild.id][key])
        for line in textwrap.wrap(text, 1994):
            line = line.replace('NEWLINE','\n')
            await ctx.send("``{}``".format(line))
            await asyncio.sleep(1)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("settings/prefixes.txt") as f:
            prefixes = eval(f.read())
            prefix = prefixes.get(message.guild.id, self.bot.default_prefix)
        if message.content.startswith(prefix):
            f = open("cogs/custom/commands.txt")
            commands = eval(f.read())
            if message.guild.id not in commands:
                commands[message.guild.id] = '{}'
                f = open("cogs/custom/commands.txt","w")
                f.write("commands")
                f.flush()
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
            