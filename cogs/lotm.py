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
                
                embed.add_field(name="Gender", value=character.gender or "Unknown", inline=True)
                
                spec_val = ", ".join(character.species) if isinstance(character.species, list) else (character.species or "Unknown")
                embed.add_field(name="Species", value=spec_val, inline=True)
                embed.add_field(name="Birth", value=character.birth or "Unknown", inline=True)
                
                pathway_val = ", ".join(character.pathways) if character.pathways else "None"
                embed.add_field(name="Pathway(s)", value=pathway_val, inline=False)
                
                titles_val = ", ".join(character.titles) if character.titles else "None"
                embed.add_field(name="Titles", value=titles_val, inline=False)

            elif category == "profile":
                origin_val = ", ".join(character.origin) if character.origin else "Unknown"
                embed.add_field(name="Birth Place / Origin", value=origin_val, inline=True)
                
                res_val = ", ".join(character.residence) if character.residence else "Unknown"
                embed.add_field(name="Residence", value=res_val, inline=True)
                
                height_val = ", ".join(character.height) if character.height else "Unknown"
                embed.add_field(name="Height", value=height_val, inline=True)
                
                hair = ", ".join(character.hair_colour) if isinstance(character.hair_colour, list) else (character.hair_colour or "Unknown")
                eyes = ", ".join(character.eye_colour) if isinstance(character.eye_colour, list) else (character.eye_colour or "Unknown")
                embed.add_field(name="Appearance", value=f"👁️ Eye: {eyes}\n💇 Hair: {hair}", inline=False)

            elif category == "mysticism":
                embed.color = 0xF59E0B
                
                if character.honorific_name:
                    poetry = "\n".join(character.honorific_name)
                    embed.description = f"### Honorific Name\n>>> {poetry}"
                
                auth_val = ", ".join(character.authorities) if character.authorities else "None"
                embed.add_field(name="Authorities / Domains", value=auth_val, inline=False)
                
                if character.symbol and "does not have" not in character.symbol:
                    embed.set_image(url=character.symbol)

            elif category == "relations":
                embed.add_field(name="Allies", value=", ".join(character.allies) if character.allies else "None", inline=False)
                embed.add_field(name="Enemies", value=", ".join(character.enemies) if character.enemies else "None", inline=False)
                
                rel_val = ", ".join(character.relatives) if character.relatives else "None"
                embed.add_field(name="Relatives", value=rel_val, inline=True)
                
                masters_val = ", ".join(character.masters) if character.masters else "None"
                embed.add_field(name="Masters", value=masters_val, inline=True)
                
                aff_val = ", ".join(character.affiliation) if character.affiliation else "None"
                embed.add_field(name="Affiliation", value=aff_val, inline=False)

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
