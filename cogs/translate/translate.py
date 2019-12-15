import discord
from discord.ext import commands
import googletrans
from googletrans import Translator

def setup(bot):
    bot.add_cog(translate(bot))

class translate(commands.Cog):
    """Translate cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self,ctx,*text):
        """Translate."""
        translator = Translator()
        srcLanguage = None
        destLanguage = 'en'
        translateThis = ''
        for word in text:
            if word.startswith("src="):
                if word.replace("src=","") in googletrans.LANGCODES.values():
                    srcLanguage = word.replace("src=","")
                elif word.replace("src=","") in googletrans.LANGCODES.keys():
                    srcLanguage = googletrans.LANGCODES[word.replace("src=","")]
                else:
                    pass
            elif word.startswith("dest="):
                if word.replace("dest=","") in googletrans.LANGCODES.values():
                    destLanguage = word.replace("dest=","")
                elif word.replace("dest=","") in googletrans.LANGCODES.keys():
                    destLanguage = googletrans.LANGCODES[word.replace("dest=","")]
                else:
                    pass
            else:
                translateThis += word+" "
        if translateThis == '':
            await ctx.send("The message can't be blank!")
            return
        translateThis = translateThis[:-1]
        if srcLanguage != None:
            translated = translator.translate(translateThis,dest=destLanguage,src=srcLanguage)
        else:
            translated = translator.translate(translateThis,dest=destLanguage)
        embed = discord.Embed(title="Translation", colour=discord.Colour(0x188079))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"Original ({googletrans.LANGUAGES[translated.src]})", value=f"{translated.origin}", inline=True)
        embed.add_field(name=f"Translated ({googletrans.LANGUAGES[translated.dest]})", value=f"{translated.text}", inline=True)
        await ctx.send(translated.text,embed=embed)

    @commands.command()
    async def listLanguages(self,ctx):
        languages = googletrans.LANGUAGES
        langText = ''
        number = 0
        for lang in list(languages.keys()):
            langText += f"{lang} - {languages[lang]} "
            number += 1
            if number < 5:
                langText += "| "
            else:
                langText += "\n"
                number = 0
        await ctx.send(langText[:-2])
