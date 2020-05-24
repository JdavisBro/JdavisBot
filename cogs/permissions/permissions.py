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
            json.dump(permissions,f,sort_keys=True, indent=4)
        return permissions

def getPermissions():
    with open("cogs/permissions/permissions.json","r+") as f:
        return json.load(f)

class permissions(commands.Cog):
    """Permissions cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="permissions",aliases=["permission","p","perms"])
    @commands.has_permissions(manage_guild=True)
    async def cmd_permissions(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cmd_permissions.command(name="add",aliases=["new"])
    async def cmd_permissions_add(self,ctx,command,role:discord.Role,channel:discord.TextChannel="*"):
        if command not in [command.name for command in list(self.bot.commands)]:
            await ctx.send(f"I was unable to find the command '{command}'")
            return
        permissions = getPermissionsAndCheckForGuildAndCommand(ctx,command)
        guildid = str(ctx.guild.id)
        roleid = str(role.id)
        if channel == "*":
            channelid = "*"
        else:
            channelid = str(channel.id)
        if roleid not in permissions[guildid][command]:
            permissions[guildid][command][roleid] = []
        if "*" in permissions[guildid][command][roleid]:
            permissions[guildid][command][roleid].remove("*")
        if channelid in permissions[guildid][command][roleid]:
            await ctx.send(f"{channel} is already in {role}'s {command} permissions.")
            return
        permissions[guildid][command][roleid].append(channelid)
        with open("cogs/permissions/permissions.json","r+") as f:
            json.dump(permissions,f,sort_keys=True, indent=4)
        await ctx.send(f"{role} now has permission to use {command} in {channel}.")

    @cmd_permissions.command(name="remove",aliases=["del","delete"])
    async def cmd_permissions_remove(self,ctx,command,role:discord.Role,channel:discord.TextChannel="*"):
        if command not in [command.name for command in list(self.bot.commands)]:
            await ctx.send(f"I was unable to find the command '{command}'")
            return
        permissions = getPermissionsAndCheckForGuildAndCommand(ctx,command)
        guildid = str(ctx.guild.id)
        if role == "*":
            roleid = "*"
        else:
            roleid = str(role.id)
        channelid = str(channel.id)
        permissions[guildid][command][roleid].pop(channelid)
        with open("cogs/permissions/permissions.json","r+") as f:
            json.dump(permissions,f,sort_keys=True, indent=4)
        await ctx.send(f"{role} no longer has permission to use {command} in {channel}.")

    @cmd_permissions.group(name="list",aliases=["ls"])
    async def cmd_permissions_list(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cmd_permissions_list.command(name="commands")
    async def cmd_permissions_list_commands(self,ctx):
        guildid = str(ctx.guild.id)
        permissions = getPermissions()
        commands = list(permissions[guildid].keys())
        await ctx.send(" - ".join(commands))

    @cmd_permissions_list.command(name="roles")
    async def cmd_permissions_list_roles(self,ctx,command):
        guildid = str(ctx.guild.id)
        permissions = getPermissions()
        roles  = [ctx.guild.get_role(int(roleid)) for roleid in permissions[guildid][command]]
        rolenames = [role.name for role in roles]
        roleids = [str(role.id) for role in roles]
        channelLists = [permissions[guildid][command][roleid] for roleid in roleids]
        channels = []
        for channelList in channelLists:
            currentChannelList = ""
            for channel in channelList:
                if channel == "*":
                    currentChannelList = "* - "
                    break
                else:
                    currentChannelList += self.bot.get_channel(int(channel)).mention + " - "
            channels.append(currentChannelList[:-3])
        embed = discord.Embed()
        embed.add_field(name="Name:", value="\n".join(rolenames), inline=True)
        embed.add_field(name="ID:", value="\n".join(roleids), inline=True)
        embed.add_field(name="Channels:", value="\n".join(channels), inline=True)
        await ctx.send(embed=embed)

    async def bot_check_once(self,ctx):
        guildid = str(ctx.guild.id)
        command = ctx.command.name
        roles = [str(role.id) for role in list(ctx.author.roles)[0:]]
        channelid = str(ctx.channel.id)
        permissions = getPermissions()
        if guildid in permissions:
            if command in permissions[guildid]:
                if "*" in permissions[guildid][command]:
                    if "*" not in permissions[guildid][command]["*"] or channelid not in permissions[guildid][command]["*"]:
                        await ctx.message.add_reaction("❎")
                        return False
                else:
                    for role in roles:
                        if role in permissions[guildid][command]:
                            if "*" not in permissions[guildid][command][role] and channelid not in permissions[guildid][command][role]:
                                await ctx.message.add_reaction("❎")
                                return False
                            else:
                                return True
                    await ctx.message.add_reaction("❎")
                    return False
        return True