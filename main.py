import os
import socket
import aiohttp
from dotenv import load_dotenv
from disnake.ext import commands
import disnake

load_dotenv()

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

sync = commands.CommandSyncFlags()
sync.all()

bot = commands.InteractionBot(reload=True, command_sync_flags=sync)

# Override login to instantiate the connector inside the active event loop
original_login = bot.login
async def custom_login(token: str):
    if bot.http.connector is None:
        bot.http.connector = aiohttp.TCPConnector(family=socket.AF_INET)
    return await original_login(token)

bot.login = custom_login

# Get the path to the "cogs" folder
cogs_folder = os.path.join(os.path.dirname(__file__), 'cogs')


# Load all the cogs in the "cogs" folder
for filename in os.listdir(cogs_folder):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        
from keep_alive import start_keep_alive

# Start the keep-alive HTTP server (runs in a daemon thread)
start_keep_alive()

bot.run(os.getenv('BOT_TOKEN'))
