import discord
from discord.ext import commands
import random
import logging

def setup(bot):
    bot.add_cog(mod(bot))
logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO) 
try:
    open("settings/mod.txt","x")
    open("settings/mod.txt","w").write('{}')
    logging.info("mod.txt created.")
except:
    logging.info("mod.txt found.")

def getmodsetting(guildid,setting):
    with open("settings/mod.txt") as f:
        settings = eval(f.read())
        if guildid not in settings:
            settings[guildid] = {}
            fw = open("settings/mod.txt","w")
            fw.write(str(settings))
            fw.flush()
        if setting not in settings[guildid]:
            setting = None
            return setting
        else:
            setting = settings[guildid][setting]
            return setting
        
class mod(commands.Cog):
    """Mod cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def modset(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @modset.command()
    async def logchannel(self,ctx,channel: discord.TextChannel):
        setting = ''
        getmodsetting(ctx.guild.id,'logchannel')
        logchannel = self.bot.get_channel(setting)
        if logchannel == channel:
            await ctx.send("The log channel is already that channel!")
        if not channel.permissions_for(ctx.guild.me).read_messages or not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("I can't read and/or send messages in that channel.")
        settings = eval(open('settings/mod.txt').read())
        settings[ctx.guild.id]['logchannel'] = channel.id
        fw = open("settings/mod.txt","w")
        fw.write(str(settings))
        fw.flush()
        await ctx.send("{} has been made the log channel".format(channel.name))
        

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def role(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @role.command(name = 'add',no_pm=True)
    async def role_add(self,ctx,role: discord.Role,user: discord.Member = ''):
        if user == '':
            user = ctx.author
        await user.add_roles(role)
        await ctx.send("{} has been given the {} role.".format(user,role))
    
    @role.command(name = 'remove')
    async def role_remove(self,ctx,role: discord.Role,user: discord.Member = ''):
        if user == '':
            user = ctx.author
        await user.remove_roles(role)
        await ctx.send("{} has been removed from the {} role".format(user,role))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,ctx,user: discord.Member,days: str = None,*,reason: str = None):
        """Bans user and deletes days of messages.
        If days (number) not stated but a word is there
        it will be treated as the first word of reason"""
        if ctx.author == user:
            await ctx.send("You can't ban yourself!")
            return
        if user == ctx.guild.owner:
            await ctx.send("You can't ban the server owner!")
            return
        usertoprole = user.top_role
        authortoprole = ctx.author.top_role
        if usertoprole > authortoprole:
            await ctx.send("That user has a role higher than you so you can't ban them!")
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
        logchannel = None
        try:
            logchannel = self.bot.get_channel(getmodsetting(ctx.guild.id,'logchannel'))
        except:
            pass
        try:
            await ctx.guild.ban(user,reason=reason,delete_message_days=days)
            await ctx.send("Banned.")
        except discord.Forbidden:
            await ctx.send("I was unable to ban that person.")
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
        if usertoprole > authortoprole:
            await ctx.send("That user has a role higher than you so you can't kick them!")
            return
        logchannel = None
        try:
            logchannel = self.bot.get_channel(getmodsetting(ctx.guild.id,'logchannel'))
        except:
            pass
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
