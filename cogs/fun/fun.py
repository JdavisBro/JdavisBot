import discord
from discord.ext import commands
import random,logging,io
from PIL import Image

def setup(bot):
    bot.add_cog(fun(bot))

class fun(commands.Cog):
    """Fun cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="fun",aliases=["f"])
    async def grp_fun(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @grp_fun.command(name="coolness",aliases=["cool"])
    async def grp_fun_coolness(self,ctx,*,user:discord.Member=None):
        if not user:
            user = ctx.author
        if user != ctx.guild.me:
            random.seed(user.id)
            if user.bot:
                if random.random() != 0:
                    await ctx.send(f"{user.display_name} is {round(random.random()*100/2,2)}% cool! (half as cool as usual because they're a bot)")
                else:
                    await ctx.send(f"{user.display_name} is {round(random.random()*100,2)}% cool! (half as cool as usual because they are a bot)")
            else:
                await ctx.send(f"{user.display_name} is {round(random.random()*100,2)}% cool!")
            random.seed()
        else:
            await ctx.send("I am 100% cool")

    @grp_fun.command(name="worm",aliases=["wormonastring","woas","string"])
    async def grp_fun_worm(self,ctx,*,user:discord.Member=None):
        if not user:
            user = ctx.author
        image,wormColour = await self.get_worm(user.id)
        await ctx.send(f"{user.display_name} is a {discord.Colour.from_rgb(wormColour[0],wormColour[1],wormColour[2])} coloured worm!",file=image)

    @grp_fun.command(name="wormid",aliases=["wormonastringid","woasid","stringid"],hidden=True)
    async def grp_fun_wormid(self,ctx,*,id:int):
        image,wormColour = await self.get_worm(id)
        await ctx.send(f"{id} is a {discord.Colour.from_rgb(wormColour[0],wormColour[1],wormColour[2])} coloured worm!",file=image)

    async def get_worm(self,id):
        random.seed(id)
        wormColour = (random.randint(1,255),random.randint(1,255),random.randint(1,255),255)
        random.seed()
        im = Image.open("cogs/fun/worm.png")
        im = im.convert("RGBA")
        pixels = im.load()
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if pixels[x,y] == (255,0,0,255):
                    pixels[x,y] = wormColour
        arr = io.BytesIO()
        im.save(arr, format='PNG')
        arr.seek(0)
        return discord.File(arr,filename="worm.png"),wormColour

    @grp_fun.command()
    async def amidumbandstupid(self,ctx,*,user:discord.Member=None):
        if user == None or user == ctx.author:
            await ctx.send("You are dumb and stupid")
        else:
            await ctx.send(f"{user.display_name} is dumb and stupid")