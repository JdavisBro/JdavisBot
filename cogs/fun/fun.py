import discord
from discord.ext import commands
import random,logging,io,requests
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

    @grp_fun.command(name="wormcolour",aliases=["wormcolor"])
    async def grp_fun_wormcolour(self,ctx,r:int,g:int,b:int):
        colour = (r,g,b,255)
        image,wormColour = await self.get_worm(colour,True)
        await ctx.send("wormColour coloured worm!",file=image)

    async def get_worm(self,id,colour=False):
        if not colour:
            random.seed(id)
            wormColour = (random.randint(1,255),random.randint(1,255),random.randint(1,255),255)
            random.seed()
        else:
            wormColour = id
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

    @grp_fun.command(name="amidumbandstupid")
    async def grp_fun_amidumbandstupid(self,ctx,*,user:discord.Member=None):
        if user == None or user == ctx.author:
            await ctx.send("You are dumb and stupid")
        else:
            await ctx.send(f"{user.display_name} is dumb and stupid")

    @grp_fun.command(name="inspire")
    async def grp_fun_inspire(self,ctx,xmas=False):
        await ctx.channel.trigger_typing()
        if xmas:
            image_url = requests.get('http://inspirobot.me/api?generate=true&season=xmas').text
        else:
            image_url = requests.get('http://inspirobot.me/api?generate=true').text
        embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))).set_image(url=image_url)
        embed.set_footer(text="inspirobot.me")
        await ctx.send(embed=embed)

    @grp_fun.command(name="fact")
    async def grp_fun_fact(self,ctx,animal):
        "koala, bird, fox, panda, dog and cat"
        animal = animal.lower()
        if animal not in ["koala","bird","fox","panda","dog","cat"]:
            await ctx.send(f"You can't get a{'n' if animal[0] in ['a','e','i','o','u'] else ''} {animal} fact! It must be either koala, bird, fox, panda, dog or cat")
            return
        await ctx.channel.trigger_typing()
        fact = requests.get(f'https://some-random-api.ml/facts/{animal}').json()["fact"]
        embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)),title=f"Fact about {animal}: {fact}")
        embed.set_footer(text="some-random-api.ml")
        await ctx.send(embed=embed)

    @grp_fun.command(name="image")
    async def grp_fun_image(self,ctx,animal):
        "koala, birb, fox, red_panda, panda, dog and cat"
        animal = animal.lower()
        if animal not in ["koala","birb","fox","red_panda","panda","dog","cat"]:
            await ctx.send(f"You can't get a{'n' if animal[0] in ['a','e','i','o','u'] else ''} {animal} image! It must be either koala, birb, fox, red_panda, panda, dog or cat")
            return
        await ctx.channel.trigger_typing()
        image = requests.get(f'https://some-random-api.ml/img/{animal}').json()["link"]
        embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)),title=f"Random {animal.replace('_',' ')} image:",url=image).set_image(url=image)
        embed.set_footer(text="some-random-api.ml")
        await ctx.send(embed=embed)