import mystic
import disnake
from disnake.ext import commands


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="name", description="Returns the name of the character.")
    async def name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        names = character.get_name()
        await ctx.send('\n'.join(f'{i+1}. {name}' for i, name in enumerate(names)))

    @commands.slash_command(name="chinese_name", description="Returns the Chinese names of the character.")
    async def chinese_name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        names = character.chinese_name
        await ctx.send(names)

    @commands.slash_command(name="birth", description="Returns the birth of the character.")
    async def birth(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        birth_dates = character.birth
        await ctx.send((birth_dates))

    @commands.slash_command(name="gender", description="Returns the gender of the character.")
    async def gender(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send(character.gender)

    @commands.slash_command(name="species", description="Returns the species of the character.")
    async def species(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        species_list = character.species
        await ctx.send('\n'.join(f'{i+1}. {species}' for i, species in enumerate(species_list)))

    @commands.slash_command(name="height", description="Returns the height of the character.")
    async def height(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        heights = character.height
        await ctx.send('\n'.join(f'{i+1}. {height}' for i, height in enumerate(heights)))

    @commands.slash_command(name="eye_colour", description="Returns the eye colour of the character.")
    async def eye_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        eye_colours = character.eye_colour
        await ctx.send('\n'.join(f'{i+1}. {eye_colour}' for i, eye_colour in enumerate(eye_colours)))

    @commands.slash_command(name="hair_colour", description="Returns the hair colour of the character.")
    async def hair_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        hair_colours = character.hair_colour
        await ctx.send('\n'.join(f'{i+1}. {hair_colour}' for i, hair_colour in enumerate(hair_colours)))

    @commands.slash_command(name="aliases", description="Returns the aliases of the character.")
    async def aliases(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        aliases = mystic.Character(character_name).aliases
        print(aliases)
        await ctx.send('\n'.join(f'{i+1}. {alias}' for i, alias in enumerate((aliases))))

    @commands.slash_command(name="titles", description="Returns the titles of the character.")
    async def titles(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {title}' for i, title in enumerate(character.titles)))

    @commands.slash_command(name="pathways", description="Returns the pathways of the character.")
    async def pathways(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {pathway}' for i, pathway in enumerate(character.pathways)))

    @commands.slash_command(name="authorities", description="Returns the authorities of the character.")
    async def authorities(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {authority}' for i, authority in enumerate(character.authorities)))

    @commands.slash_command(name="relatives", description="Returns the relatives of the character.")
    async def relatives(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {relative}' for i, relative in enumerate(character.relatives)))

    @commands.slash_command(name="masters", description="Returns the masters of the character.")
    async def masters(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {master}' for i, master in enumerate(character.masters)))

    @commands.slash_command(name="enemies", description="Returns the enemies of the character.")
    async def enemies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {enemy}' for i, enemy in enumerate(character.enemies)))

    @commands.slash_command(name="allies", description="Returns the allies of the character.")
    async def allies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {ally}' for i, ally in enumerate(character.allies)))

    @commands.slash_command(name="image", description="Returns the image of the character.")
    async def image(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send(character.image)

    @commands.slash_command(name="affliation", description="Returns the affliation of the character.")
    async def affliation(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {affliate}' for i, affliate in enumerate(character.affliation)))
    
    @commands.slash_command(name="occupation", description="Returns the occupation of the character.")
    async def occupation(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {occupation}' for i, occupation in enumerate(character.occupation)))

    @commands.slash_command(name="religion", description="Returns the religion of the character.")
    async def religion(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {religion}' for i, religion in enumerate(character.religion)))

    @commands.slash_command(name="residence", description="Returns the Residence of the character.")
    async def residence(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {resident}' for i, resident in enumerate(character.residence)))

    @commands.slash_command(name="origin", description="Returns the origin of the character.")
    async def origin(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {origin}' for i, origin in enumerate(character.origin)))
    
    @commands.slash_command(name="intro", description="Returns the Introduction of the character.")
    async def sefirots(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(f'{i+1}. {intro}' for i, intro in enumerate(character.intro)))
    
    @commands.slash_command(name="honorific_name", description="Returns the Honorific name of the character.")
    async def honorific_name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send('\n'.join(character.honorific_name))

    @commands.slash_command(name="symbol" , description="Returns the Symbol of the character.")
    async def symbol(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        character = mystic.Character(character_name)
        await ctx.send(character.symbol)

    


def setup(bot):
    bot.add_cog(CharacterCommands(bot))
