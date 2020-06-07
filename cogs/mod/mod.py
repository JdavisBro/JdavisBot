import discord
from discord.ext import commands
import random,json
import logging,re,asyncio

def setup(bot):
    bot.add_cog(mod(bot))

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO) 

try:
    open("settings/mod.json","x")
    json.dump(dict(),open("settings/mod.json","w"))
    logging.info("mod.json created.")
except:
    logging.info("mod.json found.")

try:
    open("cogs/mod/persists.json","x")
    json.dump(dict(),open("cogs/mod/persists.json","w"))
    logging.info("persists.json created.")
except:
    logging.info("persists.json found.")
        
async def adduserpersist(self,ctx,user,role):
    guildid = str(ctx.guild.id)
    userid = str(user.id)
    roleid = str(role.id)
    with open("cogs/mod/persists.json") as f:
        persists = json.load(f)
        if guildid not in persists:
            persists[guildid] = {}
            with open("cogs/mod/persists.json","w") as fw:
                json.dump(persists,fw)
        if userid not in persists[guildid]:
            persists[guildid][userid] = []
        if roleid in persists[guildid][userid]:
            return f"{user} already has {role} on their persist list!"
        persists[guildid][userid].append(roleid)
        with open("cogs/mod/persists.json","w") as fw:
            json.dump(persists,fw)
        return f"{user} will now be given {role} when they rejoin (until you remove it from them with `{prefix(self,ctx.message)}role remove '{role.name}' '{user.name}''`)"

async def deluserpersist(self,ctx,user,role):
    guildid = str(ctx.guild.id)
    userid = str(user.id)
    roleid = str(role.id)
    with open("cogs/mod/persists.json") as f:
        persists = json.load(f)
        persists[guildid][userid].remove(roleid)
        with open("cogs/mod/persists.json","w") as fw:
            json.dump(persists,fw)
        return f"{user} will no longer be given {role} when they rejoin."


def prefix(self, message):
    with open("settings/prefixes.json","r") as f:
        prefixes = json.load(f)
        guildprefix = prefixes.get(str(message.guild.id), self.bot.default_prefix)
        return guildprefix


class mod(commands.Cog):
    """Mod cog!"""

    def __init__(self, bot):
        self.bot = bot

    def getmodsetting(self,guildid,setting):
        guildid = str(guildid)
        with open("settings/mod.json") as f:
            settings = json.load(f)
            if guildid not in settings:
                settings[guildid] = {}
                with open("settings/mod.json","w") as f:
                    json.dump(settings,f)
            if setting not in settings[guildid]:
                setting = None
                return setting
            else:
                setting = settings[guildid][setting]
                return setting

    def getuserpersists(self,guildid,userid):
        guildid = str(guildid)
        userid = str(userid)
        with open("cogs/mod/persists.json") as f:
            persists = json.load(f)
            if guildid not in persists:
                persists[guildid] = {}
                with open("cogs/mod/persists.json","w") as fw:
                    json.dump(persists,fw)
            if userid not in persists[guildid]:
                return None
            else:
                return persists[guildid][userid]

    @commands.group(name="mod")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def modset(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @modset.command()
    async def logchannel(self,ctx,channel: discord.TextChannel=None):
        guildid = str(ctx.guild.id)
        setting = self.getmodsetting(guildid,'logchannel')
        try:
            logchannel = self.bot.get_channel(int(setting))
        except:
            logchannel = None
        if logchannel == channel:
            await ctx.send("The log channel is already that channel!")
            return
        if not channel.permissions_for(ctx.guild.me).read_messages or not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("I can't read and/or send messages in that channel.")
            return
        with open("settings/mod.json","r+") as f:
            settings = json.load(f)
        settings[guildid]['logchannel'] = channel.id
        with open("settings/mod.json","w+") as f:
            json.dump(settings,f)
        if channel:
            await ctx.send("{} has been made the log channel".format(channel.name))
        else:
            await ctx.send("The log channel has been removed")
        
    @modset.command(name="prefix")
    async def setprefix(self,ctx,prefix="-"):
        guildid = str(ctx.guild.id)
        with open("settings/prefixes.json","r+") as f:
            prefixes = json.load(f)
        if guildid not in prefixes:
            with open("settings/prefixes.json","r+") as f:
                prefixes[guildid] = self.bot.default_prefix
                json.dump(prefixes,f)
        if prefix == prefixes[guildid]:
            await ctx.send("That's already the prefix!")
            return
        if len(prefix) > 14:
            await ctx.send("That's too long! It must be under 15 characters.")
            return
        with open("settings/prefixes.json","w+") as f:
            prefixes[guildid] = prefix
            json.dump(prefixes,f)
            await ctx.send(f"Prefix has been set to ``{prefix}``!")

    @modset.command(name="invitecensoring",aliases=["invites"])
    async def modset_invitecensoring(self,ctx,enabled:bool=True):
        guildid = str(ctx.guild.id)
        with open("settings/mod.json","r+") as f:
            settings = json.load(f)
        if guildid not in settings:
            with open("settings/nod.json","r+") as f:
                settings[guildid] = {}
                json.dump(settings,f)
        if "invite" not in settings[guildid]:
            with open("settings/nod.json","r+") as f:
                settings[guildid] ["invite"] = True
                json.dump(settings,f)
        if enabled == settings[guildid]["invite"]:
            await ctx.send("That's already the setting!")
            return
        with open("settings/mod.json","w+") as f:
            settings[guildid]["invite"] = enabled
            json.dump(settings,f)
            await ctx.send(f"Invite Censoring has been set to {enabled}!")

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def role(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @role.command(name = 'add',no_pm=True)
    async def role_add(self,ctx,role: discord.Role,user: discord.Member = None,persist=False):
        if not user:
            user = ctx.author
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send("I don't have permission to manage roles!")
            return
        if ctx.author.top_role <= role:
            await ctx.send("You don't have permission to give that role!")
            return
        if role >= ctx.guild.me.top_role:
            await ctx.send("I can't give that role it's higher above me!")
            return
        if persist:
            await ctx.send(await adduserpersist(self,ctx,user,role))
        if role in user.roles:
            await ctx.send(f"{user} already has {role}!")
            return
        await user.add_roles(role)
        await ctx.send("{} has been given the {} role.".format(user,role))
    
    @role.command(name = 'remove',aliases=["del","rm"])
    async def role_remove(self,ctx,role: discord.Role,user: discord.Member = None):
        if not user:
            user = ctx.author
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send("I don't have permission to manage roles!")
            return
        if ctx.author.top_role <= role:
            await ctx.send("You don't have permission to take remove role!")
            return
        if role >= ctx.guild.me.top_role:
            await ctx.send("I can't remove that role it's higher above me!")
            return
        if str(role.id) in self.getuserpersists(ctx.guild.id,user.id):
            await ctx.send(await deluserpersist(self,ctx,user,role))
        if role not in user.roles:
            await ctx.send(f"{user} doesn't have {role}!")
            return
        await user.remove_roles(role)
        await ctx.send("{} has been removed from the {} role".format(user,role))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def mute(self,ctx,length,reason,*users: discord.Member):
        for roles in ctx.guild.roles:
            if roles.name == "Muted" or roles.name == "muted":
                role = roles
                break
        if role == None:
            await ctx.send(f"""I couldn't find a role named "Muted", Reply with "create" if you would like me to create one or use the `{prefix(self,ctx.message)}mod muterole ROLE` command to set your own one.""")
            def check(m):
                return (m.content.lower() == "create" or m.content.lower() == "no") and m.channel == ctx.channel and m.author == ctx.author
            try:
                await self.bot.wait_for('message',check=check,timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("Timed Out. Not creating.")
            else:
                logging.info("blah blah make role here")
        for user in users:
            if not user:
                user = ctx.author
            if not ctx.guild.me.guild_permissions.manage_roles:
                await ctx.send("I don't have permission to manage roles!")
                return
            if ctx.author.top_role <= role:
                await ctx.send("You don't have permission to take remove role!")
                return
            if role >= ctx.guild.me.top_role:
                await ctx.send("I can't remove that role it's higher above me!")
                return
            await adduserpersist(self,ctx,user,role)
            await user.add_roles(role)
            await ctx.send(f"*{user} has been muted!*")            

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,ctx,days: str = None,reason: str = None,*users: discord.Member):
        """Bans user and deletes days of messages.
        If days is a word it will be treated 
        as the first word of the reason"""
        for user in users:
            if ctx.author == user:
                await ctx.send(f"You can't ban yourself ({user})!")
                return
            if user == ctx.guild.owner:
                await ctx.send(f"You can't ban the server owner! ({user})")
                return
            usertoprole = user.top_role
            authortoprole = ctx.author.top_role
            if usertoprole >= authortoprole:
                await ctx.send(f"That user has a role higher than or equal to you so you can't ban them! ({user})")
                return
            try:
                days = int(days)
            except:
                if reason:
                    reason = days + ' ' + reason
                days = 0
            else:
                if days > 7 or days < 0:
                    await ctx.send("Days must be between 0 and 7")
            logchannel = self.bot.get_channel(self.getmodsetting(str(ctx.guild.id),'logchannel'))
            try:
                await ctx.guild.ban(user,reason=reason,delete_message_days=days)
                await ctx.send(f"Banned {user}.")
            except discord.Forbidden:
                await ctx.send(f"I was unable to ban that {user}.")
            try:
                colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
                embed = discord.Embed(title="User Banned", colour=colour)
                embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                embed.add_field(name="User:", value=str(user),inline=False)
                embed.add_field(name="Days deleted:", value=str(days),inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                await logchannel.send(embed=embed)
            except:
                pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def kick(self,ctx,user: discord.Member,*,reason: str = None):
        """Kicks user for reason"""
        if ctx.author == user:
            await ctx.send("You can't kick yourself!")
            return
        if user == ctx.guild.owner:
            await ctx.send("You can't kick the server owner!")
            return
        usertoprole = user.top_role
        authortoprole = ctx.author.top_role
        if usertoprole >= authortoprole:
            await ctx.send("That user has a role higher than or equal to you so you can't kick them!")
            return
        logchannel = self.bot.get_channel(self.getmodsetting(ctx.guild.id,'logchannel'))
        try:
            await ctx.guild.kick(user,reason=reason)
            await ctx.send("Kicked.")
        except discord.Forbidden:
            await ctx.send("I was unable to kick that person.")
        try:
            colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
            embed = discord.Embed(title="User Kicked", colour=colour)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            embed.add_field(name="User:", value=str(user),inline=False)
            embed.add_field(name="Reason:", value=reason, inline=False)
            await logchannel.send(embed=embed)
        except:
            pass

    @commands.command()
    async def roleinfo(self,ctx,*,role: discord.Role):
        listsep = 'No'
        mentionable = 'No'
        if role.hoist:
            listsep = 'Yes'
        if role.mentionable:
            mentionable = 'Yes'
        if str(role.colour) == '#000000':
            colour = '#000000 / NONE'
        else:
            colour = role.colour 
        embed = discord.Embed(title=str(role),description="<@&{}>".format(role.id),colour=role.colour)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Role ID:", value=role.id,inline=True)
        embed.add_field(name="Seperated in list:", value=listsep)
        embed.add_field(name="Role Position", value=role.position,inline=True)
        embed.add_field(name="Mentionable:", value=mentionable)
        embed.add_field(name="Colour:", value=colour)
        embed.add_field(name="Creation Time:", value=role.created_at,inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=["user","whois"])
    async def userinfo(self,ctx,*,user: discord.Member=None):
        if not user:
            user = ctx.author
        if user.is_on_mobile():
            mobile = "Yes"
        else:
            mobile = "No"
        for role in user.roles:
            if role.name == "@everyone":
                everyoneRole = role.mention
                break
        roles = [role.mention for role in user.roles]
        roles.remove(everyoneRole)
        permissions = []
        for permission in list(user.guild_permissions):
            if permission[1] == True:
                permissions.append(permission[0])
        if "administrator" in permissions:
            permissions = ["administrator"]
        joinposition = sum(m.joined_at < user.joined_at for m in ctx.guild.members if m.joined_at is not None)+1
        embed = discord.Embed(title=str(user),description="<@{}>".format(user.id),color=user.colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="User ID:", value=user.id,inline=True)
        embed.add_field(name="Joined Here:", value=user.joined_at,inline=True)
        embed.add_field(name="Created:", value=user.created_at,inline=True)
        embed.add_field(name="On Mobile:", value=mobile,inline=True)
        embed.add_field(name="Join Position:", value=joinposition,inline=True)
        embed.add_field(name=f"Roles [{len(roles)}]:",value=" - ".join(roles),inline=False)
        embed.add_field(name="Permissions:", value=" - ".join(permissions),inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["members"])
    async def membercount(self,ctx):
        embed = discord.Embed(title=f"There are {ctx.guild.member_count} members!", colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.discriminator == "0000":
            return
        if isinstance(message.channel,discord.TextChannel):
            # INVITE CENSORSHIP
            if message.type == discord.MessageType.default:
                if self.getmodsetting(message.guild.id,"invite") or self.getmodsetting(message.guild.id,"invite") is None:
                    if not message.author.permissions_in(message.channel).manage_guild:
                        if re.search(r"discord.gg/\S",message.content) or re.search(r"discord.com/invite/\S",message.content) or re.search(r"discordapp.com/invite/\S",message.content):
                            await message.delete()
                            await message.channel.send(f"{message.author.mention}, no invite links!",delete_after=5)
                            if self.getmodsetting(message.guild.id,"logchannel"):
                                colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
                                embed = discord.Embed(title="User send an invite.", colour=colour)
                                embed.add_field(name="User:", value=str(message.author),inline=False)
                                embed.add_field(name="Message:", value=message.content, inline=False)
                                await self.bot.get_channel(self.getmodsetting(message.guild.id,"logchannel")).send(embed=embed)
            if message.type == discord.MessageType.new_member:
                await message.add_reaction("🎉")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        persists = self.getuserpersists(member.guild.id,member.id)
        if persists:
            roles = [member.guild.get_role(int(roleid)) for roleid in persists]
            await asyncio.sleep(0.5)
            await member.add_roles(*roles)
