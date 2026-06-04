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

print("=== STARTING DIAGNOSTIC CHECKS ===")
try:
    print("1. Resolving discord.com...")
    resolved = socket.getaddrinfo("discord.com", 443)
    for res in resolved:
        print(f"   Family: {res[0]}, Addr: {res[4]}")
except Exception as e:
    print("   DNS Resolution failed:", e)

try:
    print("2. Testing connection to discord.com via urllib...")
    import ssl
    context = ssl.create_default_context()
    with urllib.request.urlopen("https://discord.com", timeout=10, context=context) as response:
        print("   urllib Response Status:", response.getcode())
except Exception as e:
    print("   urllib connection failed:", e)
print("=== DIAGNOSTIC CHECKS COMPLETE ===")

bot = commands.InteractionBot(reload=True, command_sync_flags=sync)

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
