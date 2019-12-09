import discord, asyncio, logging
from discord.ext import commands
import json

def setup(bot):
    bot.add_cog(custom(bot))

try:
    open("cogs/custom/commands.json","x")
    open("cogs/custom/commands.json","w").write(dict())
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
        guildid = str(ctx.guild.id)
        with open("cogs/custom/commands.json", "r+") as f:
            commandServerDict = json.load(f)
        if guildid not in commandServerDict:
            commandServerDict[guildid] = dict()
            with open("cogs/custom/commands.json", "w+") as f:
                json.dump(commandServerDict,f)
        if name in self.bot.commands:
            await ctx.send("There is already an actual command named that.")
            return
        if name in commandServerDict[guildid]:
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
        commandServerDict[guildid][name] = content
        with open("cogs/custom/commands.json","w+") as f:
            json.dump(commandServerDict,f)
        await ctx.send("Command {} added!".format(name))

    @custom.command(name="del", aliases = ['delete','remove','d'])
    @commands.has_permissions(manage_guild=True)
    async def cc_del(self,ctx,name):
        """Deltes a custom command for this server, requires manage server permission."""
        guildid = str(ctx.guild.id)
        with open("cogs/custom/commands.json", "r+") as f:
                commandServerDict = json.load(f)
        if guildid not in commandServerDict:
            commandServerDict[guildid] = dict()
            with open("cogs/custom/commands.json", "w+") as f:
                json.dump(commandServerDict,f)
            await ctx.send("{} wasn't found.".format(name))
            return
        if commandServerDict[guildid].pop(name,None) is None:
            await ctx.send("{} wasn't found.".format(name))
            return
        else:
            with open("cogs/custom/commands.json", "w+") as f:
                json.dump(commandServerDict,f)
            await ctx.send("Command {} deleted!".format(name))
        
    @custom.command(name = 'list',aliases = ['get','view','l','ls'])
    async def cc_list(self,ctx):
        """Lists custom commands for this server."""
        guildid = str(ctx.guild.id)
        with open("cogs/custom/commands.json", "r+") as f:
            commandServerDict = json.load(f)
        if guildid not in commandServerDict:
            commandServerDict[guildid] = dict()
            with open("cogs/custom/commands.json", "w+") as f:
                json.dump(commandServerDict,f)
        if not commandServerDict[guildid]:
            await ctx.send("There are no commands in this server.")
            return
        text = f'Custom Commands for {ctx.guild.name}:\n'
        for key in commandServerDict[guildid]:
            text += f'{str(key)}: {commandServerDict[guildid][key]}\n'
        for line in [text[i:i + 1990] for i in range(0, len(text), 1994)]:
            await ctx.send(f"```YML\n{line}```")
            await asyncio.sleep(1)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        guildid = str(message.guild.id)
        with open("settings/prefixes.json") as f: # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            prefixes = json.load(f)
            prefix = prefixes.get(message.guild.id, self.bot.default_prefix)
        if message.content.startswith(prefix):
            with open("cogs/custom/commands.json", "r+") as f:
                commandServerDict = json.load(f)
            if guildid not in commandServerDict:
                commandServerDict[guildid] = dict()
                with open("cogs/custom/commands.json", "w+") as f:
                    json.dump(commandServerDict,f)
                return
            text = message.content.replace(prefix,'')
            strnumber = 0
            cmd = ''
            args = ''
            text = text.split()
            for word in text:
                if strnumber == 0:
                    strnumber = 1
                    cmd = word
                else:
                    args += word + " "
            args = args[0:len(args)-1]
            if cmd not in commandServerDict[guildid]:
                return
            text = commandServerDict[guildid][cmd]
            text = text.replace("$A",args)
            await message.channel.send(text.format(message))
            