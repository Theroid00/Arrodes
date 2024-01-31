import api
import api
import disnake
from disnake.ext import commands


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="name", description="Returns the name of the character.")
    async def name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        names = character.get_name()
        await ctx.send('\n'.join(f'{i+1}. {name}' for i, name in enumerate(names)))

    @commands.slash_command(name="chinese_name", description="Returns the Chinese names of the character.")
    async def chinese_name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        names = character.chinese_name
        await ctx.send('\n'.join(f'{i+1}. {name}' for i, name in enumerate(names)))

    @commands.slash_command(name="birth", description="Returns the birth of the character.")
    async def birth(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        birth_dates = character.birth
        await ctx.send('\n'.join(f'{i+1}. {birth_date}' for i, birth_date in enumerate(birth_dates)))

    @commands.slash_command(name="gender", description="Returns the gender of the character.")
    async def gender(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        genders = character.gender
        await ctx.send('\n'.join(f'{i+1}. {gender}' for i, gender in enumerate(genders)))

    @commands.slash_command(name="species", description="Returns the species of the character.")
    async def species(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        species_list = character.species
        await ctx.send('\n'.join(f'{i+1}. {species}' for i, species in enumerate(species_list)))

    @commands.slash_command(name="height", description="Returns the height of the character.")
    async def height(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        heights = character.height
        await ctx.send('\n'.join(f'{i+1}. {height}' for i, height in enumerate(heights)))

    @commands.slash_command(name="eye_colour", description="Returns the eye colour of the character.")
    async def eye_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        eye_colours = character.eye_colour
        await ctx.send('\n'.join(f'{i+1}. {eye_colour}' for i, eye_colour in enumerate(eye_colours)))

    @commands.slash_command(name="hair_colour", description="Returns the hair colour of the character.")
    async def hair_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        hair_colours = character.hair_colour
        await ctx.send('\n'.join(f'{i+1}. {hair_colour}' for i, hair_colour in enumerate(hair_colours)))

    @commands.slash_command(name="aliases", description="Returns the aliases of the character.")
    async def aliases(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {alias}' for i, alias in enumerate(character.aliases)))

    @commands.slash_command(name="titles", description="Returns the titles of the character.")
    async def titles(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {title}' for i, title in enumerate(character.titles)))

    @commands.slash_command(name="pathways", description="Returns the pathways of the character.")
    async def pathways(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {pathway}' for i, pathway in enumerate(character.pathways)))

    @commands.slash_command(name="authorities", description="Returns the authorities of the character.")
    async def authorities(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {authority}' for i, authority in enumerate(character.authorities)))

    @commands.slash_command(name="relatives", description="Returns the relatives of the character.")
    async def relatives(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {relative}' for i, relative in enumerate(character.relatives)))

    @commands.slash_command(name="masters", description="Returns the masters of the character.")
    async def masters(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {master}' for i, master in enumerate(character.masters)))

    @commands.slash_command(name="enemies", description="Returns the enemies of the character.")
    async def enemies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {enemy}' for i, enemy in enumerate(character.enemies)))

    @commands.slash_command(name="allies", description="Returns the allies of the character.")
    async def allies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {ally}' for i, ally in enumerate(character.allies)))

    @commands.slash_command(name="image", description="Returns the image of the character.")
    async def image(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = api.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {images}' for i, images in enumerate(character.image)))

def setup(bot):
    bot.add_cog(CharacterCommands(bot))
