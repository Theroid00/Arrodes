
import os
from disnake.ext import commands
import disnake

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

sync = commands.CommandSyncFlags()
sync.all()

bot = commands.InteractionBot(reload=True, command_sync_flags=sync)

# Get the path to the "cogs" folder
cogs_folder = os.path.join(os.path.dirname(__file__), 'cogs')

# Load all the cogs in the "cogs" folder
for filename in os.listdir(cogs_folder):
    if filename.endswith('.py'):
        cog_name = filename[:-3]  # Remove the file extension
        cog_module = f'cogs.{cog_name}'
        bot.load_extension(cog_module)

bot.run('')




