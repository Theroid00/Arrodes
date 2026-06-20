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


def _format_field_value(value, fallback="None", bullet_points=False) -> str:
    """Format a string or list of strings nicely for Discord embeds."""
    if not value:
        return fallback
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        if not cleaned:
            return fallback
        if bullet_points and len(cleaned) > 2:
            return "\n".join(f"• {item}" for item in cleaned)
        return ", ".join(cleaned)
    return str(value)


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="character",
        description="Search for a Lord of the Mysteries character profile."
    )
    async def character_command(
        self, 
        ctx: disnake.ApplicationCommandInteraction, 
        character_name: str,
        category: str = commands.Param(
            default="summary",
            choices=["summary", "profile", "mysticism", "relations"]
        )
    ):
        """Displays formatted embeds for a character based on category."""
        await ctx.response.defer()
        try:
            character = await get_character(character_name)
            
            title_name = character.get_name() or character_name.title()
            if character.chinese_name:
                chinese_str = ", ".join(f"{cn} ({en})" for cn, en in character.chinese_name)
                embed_title = f"👤 {title_name} ({chinese_str})"
            else:
                embed_title = f"👤 {title_name}"

            embed = disnake.Embed(title=embed_title, color=0x6366F1)
            
            if character.image and character.image != "No Image exists yet.":
                embed.set_thumbnail(url=character.image)

            if category == "summary":
                intro_text = "\n\n".join(character.intro) if isinstance(character.intro, list) else character.intro
                if intro_text:
                    truncated_intro = intro_text[:450] + "..." if len(intro_text) > 450 else intro_text
                    embed.description = f"*{truncated_intro}*"
                
                embed.add_field(name="Gender", value=_format_field_value(character.gender, "Unknown"), inline=True)
                embed.add_field(name="Species", value=_format_field_value(character.species, "Unknown"), inline=True)
                embed.add_field(name="Birth", value=_format_field_value(character.birth, "Unknown"), inline=True)
                
                embed.add_field(name="Pathway(s)", value=_format_field_value(character.pathways, "None"), inline=False)
                embed.add_field(name="Aliases", value=_format_field_value(character.aliases, "None", bullet_points=True), inline=False)
                embed.add_field(name="Titles", value=_format_field_value(character.titles, "None", bullet_points=True), inline=False)

            elif category == "profile":
                embed.add_field(name="Birth Place / Origin", value=_format_field_value(character.origin, "Unknown"), inline=True)
                embed.add_field(name="Residence", value=_format_field_value(character.residence, "Unknown"), inline=True)
                embed.add_field(name="Height", value=_format_field_value(character.height, "Unknown"), inline=True)
                
                eyes = _format_field_value(character.eye_colour, "Unknown")
                hair = _format_field_value(character.hair_colour, "Unknown")
                embed.add_field(name="Appearance", value=f"👁️ Eye: {eyes}\n💇 Hair: {hair}", inline=False)
                
                embed.add_field(name="Occupation(s)", value=_format_field_value(character.occupation, "Unknown", bullet_points=True), inline=False)
                embed.add_field(name="Religion(s)", value=_format_field_value(character.religion, "Unknown", bullet_points=True), inline=False)

            elif category == "mysticism":
                embed.color = 0xF59E0B
                
                if character.honorific_name:
                    poetry = "\n".join(character.honorific_name)
                    embed.description = f"### Honorific Name\n>>> {poetry}"
                
                embed.add_field(name="Authorities / Domains", value=_format_field_value(character.authorities, "None", bullet_points=True), inline=False)
                
                if character.symbol and "does not have" not in character.symbol:
                    embed.set_image(url=character.symbol)

            elif category == "relations":
                embed.add_field(name="Allies", value=_format_field_value(character.allies, "None", bullet_points=True), inline=False)
                embed.add_field(name="Enemies", value=_format_field_value(character.enemies, "None", bullet_points=True), inline=False)
                embed.add_field(name="Relatives", value=_format_field_value(character.relatives, "None", bullet_points=True), inline=True)
                embed.add_field(name="Masters", value=_format_field_value(character.masters, "None", bullet_points=True), inline=True)
                embed.add_field(name="Affiliation", value=_format_field_value(character.affiliation, "None", bullet_points=True), inline=False)


            await ctx.edit_original_response(embed=embed)
            
        except NotFoundError as e:
            await ctx.edit_original_response(content=f"❌ {e}")
        except Exception as e:
            await ctx.edit_original_response(content=f"⚠️ An unexpected error occurred: {e}")

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
