import mystic
import disnake
from disnake.ext import commands
from mystic.helpers.exceptions import NotFoundError
import asyncio

# Simple in-memory caches: key -> parsed object
_character_cache: dict[str, mystic.Character] = {}
_pathway_cache: dict[str, mystic.Pathway] = {}
_artifact_cache: dict[str, mystic.SealedArtifact] = {}


async def get_character(character_name: str) -> mystic.Character:
    """Return a cached Character or fetch a new one."""
    key = character_name.lower()
    if key not in _character_cache:
        _character_cache[key] = await asyncio.to_thread(mystic.Character, character_name)
    return _character_cache[key]


async def get_pathway(pathway_name: str) -> mystic.Pathway:
    """Return a cached Pathway or fetch a new one."""
    key = pathway_name.lower()
    if key not in _pathway_cache:
        _pathway_cache[key] = await asyncio.to_thread(mystic.Pathway, pathway_name)
    return _pathway_cache[key]


async def get_artifact(artifact_name: str) -> mystic.SealedArtifact:
    """Return a cached SealedArtifact or fetch a new one."""
    key = artifact_name.lower()
    if key not in _artifact_cache:
        _artifact_cache[key] = await asyncio.to_thread(mystic.SealedArtifact, artifact_name)
    return _artifact_cache[key]


def _list_response(items) -> str:
    """Format a list of items as a numbered string."""
    if not items:
        return "No data found."
    return '\n'.join(f'{i + 1}. {item}' for i, item in enumerate(items))


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _execute_query(self, ctx: disnake.ApplicationCommandInteraction, character_name: str, extractor):
        """Helper to defer the response, fetch character, and edit the original message."""
        await ctx.response.defer()
        try:
            character = await get_character(character_name)
            data = extractor(character)
            
            if isinstance(data, list):
                content = _list_response(data)
            else:
                content = data
                
            await ctx.edit_original_response(content=content or "No information found.")
        except NotFoundError as e:
            await ctx.edit_original_response(content=f"❌ {e}")
        except Exception as e:
            await ctx.edit_original_response(content=f"⚠️ An unexpected error occurred: {e}")

    @commands.slash_command(name="name", description="Returns the name of the character.")
    async def name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.get_name() or "No name found.")

    @commands.slash_command(name="chinese_name", description="Returns the Chinese names of the character.")
    async def chinese_name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        def extract(c):
            names = c.chinese_name
            if not names:
                return "No Chinese name found."
            return '\n'.join(f'{i + 1}. {cn} ({en})' for i, (cn, en) in enumerate(names))
        await self._execute_query(ctx, character_name, extract)

    @commands.slash_command(name="birth", description="Returns the birth of the character.")
    async def birth(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.birth or "No birth information found.")

    @commands.slash_command(name="gender", description="Returns the gender of the character.")
    async def gender(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.gender or "No gender information found.")

    @commands.slash_command(name="species", description="Returns the species of the character.")
    async def species(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.species)

    @commands.slash_command(name="height", description="Returns the height of the character.")
    async def height(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.height)

    @commands.slash_command(name="eye_colour", description="Returns the eye colour of the character.")
    async def eye_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.eye_colour)

    @commands.slash_command(name="hair_colour", description="Returns the hair colour of the character.")
    async def hair_colour(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.hair_colour)

    @commands.slash_command(name="aliases", description="Returns the aliases of the character.")
    async def aliases(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.aliases)

    @commands.slash_command(name="titles", description="Returns the titles of the character.")
    async def titles(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.titles)

    @commands.slash_command(name="pathways", description="Returns the pathways of the character.")
    async def pathways(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.pathways)

    @commands.slash_command(name="authorities", description="Returns the authorities of the character.")
    async def authorities(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.authorities)

    @commands.slash_command(name="relatives", description="Returns the relatives of the character.")
    async def relatives(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.relatives)

    @commands.slash_command(name="masters", description="Returns the masters of the character.")
    async def masters(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.masters)

    @commands.slash_command(name="enemies", description="Returns the enemies of the character.")
    async def enemies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.enemies)

    @commands.slash_command(name="allies", description="Returns the allies of the character.")
    async def allies(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.allies)

    @commands.slash_command(name="image", description="Returns the image of the character.")
    async def image(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.image)

    @commands.slash_command(name="affiliation", description="Returns the affiliation of the character.")
    async def affiliation(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.affiliation)

    @commands.slash_command(name="occupation", description="Returns the occupation of the character.")
    async def occupation(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.occupation)

    @commands.slash_command(name="religion", description="Returns the religion of the character.")
    async def religion(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.religion)

    @commands.slash_command(name="residence", description="Returns the Residence of the character.")
    async def residence(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.residence)

    @commands.slash_command(name="origin", description="Returns the origin of the character.")
    async def origin(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.origin)

    @commands.slash_command(name="intro", description="Returns the Introduction of the character.")
    async def intro(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.intro)

    @commands.slash_command(name="honorific_name", description="Returns the Honorific name of the character.")
    async def honorific_name(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        def extract(c):
            names = c.honorific_name
            if not names:
                return "No honorific name found."
            return '\n'.join(names)
        await self._execute_query(ctx, character_name, extract)

    @commands.slash_command(name="symbol", description="Returns the Symbol of the character.")
    async def symbol(self, ctx: disnake.ApplicationCommandInteraction, character_name: str):
        await self._execute_query(ctx, character_name, lambda c: c.symbol)

    @commands.slash_command(name="pathway", description="Returns details about a Beyonder Pathway.")
    async def pathway_command(self, ctx: disnake.ApplicationCommandInteraction, pathway_name: str):
        """Displays details of a Beyonder Pathway, including its sequences."""
        await ctx.response.defer()
        try:
            pathway = await get_pathway(pathway_name)
            
            embed = disnake.Embed(
                title=f"🔮 {pathway.name}",
                description=pathway.overview or "No description available.",
                url=pathway.url,
                color=0x4F46E5  # Indigo
            )
            if pathway.image and pathway.image != "No image found.":
                embed.set_thumbnail(url=pathway.image)
                
            embed.add_field(name="God", value=pathway.god, inline=True)
            embed.add_field(name="Sefirah", value=pathway.sefirah, inline=True)
            embed.add_field(name="Above the Sequence", value=pathway.above_the_sequence, inline=True)
            embed.add_field(name="Mythical Form", value=pathway.mythical_form, inline=False)
            embed.add_field(name="Related Organizations", value=pathway.organizations, inline=False)
            
            if pathway.sequences:
                seq_text = "\n".join(f"**Seq {num}**: {name}" for num, name in pathway.sequences)
                embed.add_field(name="Sequence Levels", value=seq_text, inline=False)
                
            await ctx.edit_original_response(embed=embed)
        except NotFoundError as e:
            await ctx.edit_original_response(content=f"❌ {e}")
        except Exception as e:
            await ctx.edit_original_response(content=f"⚠️ An unexpected error occurred: {e}")

    @commands.slash_command(name="artifact", description="Returns details about a Sealed Artifact.")
    async def artifact_command(self, ctx: disnake.ApplicationCommandInteraction, artifact_name: str):
        """Displays details of a Sealed Artifact, including its abilities and downsides."""
        await ctx.response.defer()
        try:
            artifact = await get_artifact(artifact_name)
            
            embed = disnake.Embed(
                title=f"🗝️ {artifact.name}",
                description=artifact.overview or "No description available.",
                url=artifact.url,
                color=0xDC2626  # Red
            )
            if artifact.image and artifact.image != "No image found.":
                embed.set_thumbnail(url=artifact.image)
                
            embed.add_field(name="Chinese Name", value=artifact.chinese_name, inline=True)
            embed.add_field(name="Type", value=artifact.type, inline=True)
            embed.add_field(name="Status", value=artifact.status, inline=True)
            embed.add_field(name="Corresponding Pathway", value=artifact.corresponding_pathway, inline=False)
            embed.add_field(name="Latest Possessor(s)", value=artifact.latest_possessor, inline=False)
            embed.add_field(name="Former Possessor(s)", value=artifact.former_possessors, inline=False)
            
            # Format/Truncate fields if they exceed Discord embed limits
            power = artifact.power if len(artifact.power) < 1024 else artifact.power[:1020] + "..."
            downside = artifact.downside if len(artifact.downside) < 1024 else artifact.downside[:1020] + "..."
            
            embed.add_field(name="Magical Abilities", value=power, inline=False)
            embed.add_field(name="Side Effects / Downside", value=downside, inline=False)
            
            await ctx.edit_original_response(embed=embed)
        except NotFoundError as e:
            await ctx.edit_original_response(content=f"❌ {e}")
        except Exception as e:
            await ctx.edit_original_response(content=f"⚠️ An unexpected error occurred: {e}")


def setup(bot):
    bot.add_cog(CharacterCommands(bot))
