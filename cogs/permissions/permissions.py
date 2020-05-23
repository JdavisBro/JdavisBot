import discord
from discord.ext import commands
import logging, json

def setup(bot):
    bot.add_cog(permissions(bot))

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO) 

try:
    open("cogs/permissions/permissions.json","x")
    json.dump(dict(),open("cogs/permissions/permissions.json","w"))
    logging.info("permissions.json created.")
except:
    logging.info("permissions.json found.")

def getPermissionsAndCheckForGuildAndCommand(ctx,command):
    with open("cogs/permissions/permissions.json","r+") as f:
        permissions = json.load(f)
        if str(ctx.guild.id) not in permissions:
            permissions[str(ctx.guild.id)] = {}
        if command not in permissions[str(ctx.guild.id)]:
            permissions[str(ctx.guild.id)][command] = {"*": ["*"]}
            json.dump(permissions,f)
        return permissions

def getPermissions():
    with open("cogs/permissions/permissions.json","r+") as f:
        return json.load(f)

class permissions(commands.Cog):
    """Permissions cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="permissions",aliases=["permission","p","perms"])
    async def cmd_permissions(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cmd_permissions.command(name="add",aliases=["new"])
    async def cmd_permissions_add(self,ctx,command,role:discord.Role):
        if command not in [command.name for command in list(self.bot.commands)]:
            await ctx.send(f"I was unable to find the command '{command}'")
            return
        permissions = getPermissionsAndCheckForGuildAndCommand(ctx,command)
        guildid = str(ctx.guild.id)
        roleid = str(role.id)
        permissions[guildid][command][roleid] = ["*"]
        permissions[guildid][command].pop("*",None)
        with open("cogs/permissions/permissions.json","r+") as f:
            json.dump(permissions,f)

    @cmd_permissions.command(name="remove",aliases=["del","delete"])
    async def cmd_permissions_remove(self,ctx,command,role:discord.Role):
        if command not in [command.name for command in list(self.bot.commands)]:
            await ctx.send(f"I was unable to find the command '{command}'")
            return
        permissions = getPermissionsAndCheckForGuildAndCommand(ctx,command)
        guildid = str(ctx.guild.id)
        roleid = str(role.id)
        permissions[guildid][command].pop(roleid)
        if not permissions[guildid][command]:
            permissions[guildid][command]["*"] = ["*"]
        with open("cogs/permissions/permissions.json","r+") as f:
            json.dump(permissions,f)

    @cmd_permissions.group(name="channels",aliases=["channel"])
    async def cmd_permissions_channel(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cmd_permissions_channel.command(name="add",aliases=["new"])
    async def cmd_permissions_channel_add(self,ctx,command,role:discord.Role,channel:discord.TextChannel):
        if command not in [command.name for command in list(self.bot.commands)]:
            await ctx.send(f"I was unable to find the command '{command}'")
            return
        permissions = getPermissionsAndCheckForGuildAndCommand(ctx,command)
        guildid = str(ctx.guild.id)
        roleid = str(role.id)
        channelid = str(channel.id)
        if channelid in permissions[guildid][command][roleid]:
            await ctx.send(f"{channel.name} is already in {role.name}'s {command} permissions.")
            return
        permissions[guildid][command][roleid].append(channelid)
        if "*" in permissions[guildid][command][roleid]:
            permissions[guildid][command][roleid].remove("*")
        with open("cogs/permissions/permissions.json","r+") as f:
            json.dump(permissions,f)
        await ctx.send(f"{role.name} now has permission to use {command} in {channel.name}.")

    @cmd_permissions_channel.command(name="remove",aliases=["del","delete"])
    async def cmd_permissions_channel_remove(self,ctx,command,role:discord.Role,channel:discord.TextChannel):
        if command not in [command.name for command in list(self.bot.commands)]:
            await ctx.send(f"I was unable to find the command '{command}'")
            return
        permissions = getPermissionsAndCheckForGuildAndCommand(ctx,command)
        guildid = str(ctx.guild.id)
        roleid = str(role.id)
        channelid = str(channel.id)
        permissions[guildid][command][roleid].pop(channelid)
        with open("cogs/permissions/permissions.json","r+") as f:
            json.dump(permissions,f)
        await ctx.send(f"{role.name} no longer has permission to use {command} in {channel.name}.")


    async def bot_check_once(self,ctx):
        guildid = str(ctx.guild.id)
        command = ctx.command.name
        roles = [str(role.id) for role in list(ctx.author.roles)[1:]]
        channelid = str(ctx.channel.id)
        permissions = getPermissions()
        if guildid in permissions:
            if command in permissions[guildid]:
                if "*" in permissions[guildid][command]:
                    if "*" in permissions[guildid][command]["*"] or channelid in permissions[guildid][command]["*"]:
                        return True
                    else:
                        return False
                else:
                    for role in roles:
                        if role in permissions[guildid][command]:
                            if "*" in permissions[guildid][command][role] or channelid in permissions[guildid][command][role]:
                                return True
                            else:
                                return False
                        else:
                            return False
        return True