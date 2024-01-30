import api
import disnake
from disnake.ext import commands


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="name", description="Returns the name of the character.")
    async def name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.get_name())

    @commands.slash_command(name="chinese_name", description="Returns the Chinese name of the character.")
    async def chinese_name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.chinese_name)

    @commands.slash_command(name="birth", description="Returns the birth of the character.")
    async def birth(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.birth)

    @commands.slash_command(name="gender", description="Returns the gender of the character.")
    async def gender(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.gender)

    @commands.slash_command(name="species", description="Returns the species of the character.")
    async def species(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.species)

    @commands.slash_command(name="height", description="Returns the height of the character.")
    async def height(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.height)

    @commands.slash_command(name="eye_colour", description="Returns the eye colour of the character.")
    async def eye_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.eye_colour)

    @commands.slash_command(name="hair_colour", description="Returns the hair colour of the character.")
    async def hair_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.hair_colour)

    @commands.slash_command(name="aliases", description="Returns the aliases of the character.")
    async def aliases(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.aliases)

    @commands.slash_command(name="titles", description="Returns the titles of the character.")
    async def titles(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.titles)

    @commands.slash_command(name="pathways", description="Returns the pathways of the character.")
    async def pathways(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.pathways)

    @commands.slash_command(name="authorities", description="Returns the authorities of the character.")
    async def authorities(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.authorities)

    @commands.slash_command(name="relatives", description="Returns the relatives of the character.")
    async def relatives(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.relatives)

    @commands.slash_command(name="masters", description="Returns the masters of the character.")
    async def masters(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.masters)

    @commands.slash_command(name="enemies", description="Returns the enemies of the character.")
    async def enemies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.enemies)

    @commands.slash_command(name="allies", description="Returns the allies of the character.")
    async def allies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send(character.allies)

def setup(bot):
    bot.add_cog(CharacterCommands(bot))