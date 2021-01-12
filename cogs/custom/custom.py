import asyncio
import logging

import discord
from discord.ext import commands

import storage

def setup(bot):
    bot.add_cog(custom(bot))

if storage.create('commands',{},path="cogs/custom/")[0]:
    logging.info("cogs/custom/commands.json created.")

class custom(commands.Cog):
    """Cog to add custom commands for servers!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['cc','customcommand'])
    async def custom(self,ctx):
        """Commands to add custom commands to each server."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    async def checkGuildDict(self,guildid):
        if not storage.read("commands",path="cogs/custom/",key=[guildid]):
            storage.write("commands",{},path="cogs/custom/",key=guildid)
        return storage.read("commands",path="cogs/custom/",key=[guildid])

    @custom.command(name='add',aliases = ['new','make','a'])
    @commands.has_permissions(manage_guild=True)
    async def cc_add(self,ctx,name,*,content):
        """Adds a custom command for this server, requires manage server permissions.
        You can use arguments to the context class if you do
        {.messagearguments}. For example .guild.name .channel.id .author.display_name .
        if you want to use more than one ctx argument you add a 0, e.g {0.message.id}
        you can also add arguments that the user fills in with $A"""
        guildid = str(ctx.guild.id)
        name = name.lower()
        commands = await self.checkGuildDict(guildid)
        actualcommands = [command.name for command in self.bot.commands]
        for aliases in [command.aliases for command in self.bot.commands]:
            if aliases:
                for alias in aliases:
                    actualcommands.append(alias)
        if name in actualcommands:
            await ctx.send("There is already an actual command named that.")
            return
        if name in commands:
            await ctx.send(f"Warning: There is already a command named `{name}` in this server continuing would overwrite it.\nIf you want to continue say `yes`.")
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
        commands[name] = content
        storage.write("commands",commands,path="cogs/custom/",key=guildid)
        await ctx.send(f"Command {name} added!")

    @custom.command(name="del", aliases = ['delete','remove','d'])
    @commands.has_permissions(manage_guild=True)
    async def cc_del(self,ctx,name):
        """Deltes a custom command for this server, requires manage server permission."""
        guildid = str(ctx.guild.id)
        commands = await self.checkGuildDict(guildid)
        if commands.pop(name,None) is None:
            await ctx.send("{} wasn't found.".format(name))
            return
        else:
            storage.write("commands",commands,path="cogs/custom/",key=guildid)
            await ctx.send("Command {} deleted!".format(name))
        
    @custom.command(name = 'list',aliases = ['get','view','l','ls'])
    async def cc_list(self,ctx):
        """Lists custom commands for this server."""
        guildid = str(ctx.guild.id)
        commands = await self.checkGuildDict(guildid)
        if not commands:
            await ctx.send("There are no commands in this server.")
            return
        text = f'Custom Commands for "{ctx.guild.name}":\n'
        for key in commands:
            text += f'{str(key)}: {commands[key]}\n'
        for line in [text[i:i + 1990] for i in range(0, len(text), 1994)]:
            await ctx.send(f"```YML\n{line}```")
            await asyncio.sleep(1)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel,discord.DMChannel):
            return
        if message.author.bot:
            return
        guildid = str(message.guild.id)
        guildprefix = storage.read("prefixes",key=[str(message.guild.id)],default=self.bot.default_prefix)
        prefixes = [f"{guildprefix} ",guildprefix]        
        commands = await self.checkGuildDict(guildid)
        if not commands:
            return
        prefix = None
        for aPrefix in prefixes:
            if message.content.startswith(aPrefix):
                prefix = aPrefix
        if not prefix:
            return
        text = message.content[len(prefix)::]
        strnumber = 0
        cmd = ''
        args = ''
        text = text.split()
        for word in text:
            if strnumber == 0:
                strnumber = 1
                cmd = word.lower()
            else:
                args += word + " "
        args = args[0:len(args)-1]
        if cmd not in commands:
            return
        text = commands[cmd]
        text = text.replace("$A",args)
        await message.channel.send(text.format(message))
        