import os
from dotenv import load_dotenv
from disnake.ext import commands
import disnake

load_dotenv()

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

sync = commands.CommandSyncFlags()
sync.all()

bot = commands.InteractionBot(reload=True, command_sync_flags=sync, intents=intents)

# Load all cogs
cogs_folder = os.path.join(os.path.dirname(__file__), 'cogs')
for filename in os.listdir(cogs_folder):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

print("Starting Arrodes bot...")
bot.run(os.getenv('BOT_TOKEN'))
