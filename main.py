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
import ssl

def test_connection(family, name):
    print(f"Testing direct TCP connection to discord.com ({name})...")
    try:
        s = socket.socket(family, socket.SOCK_STREAM)
        s.settimeout(5)
        resolved = socket.getaddrinfo("discord.com", 443, family=family)
        if not resolved:
            print(f"  No {name} address resolved.")
            return
        addr = resolved[0][4]
        print(f"  Connecting to {addr}...")
        s.connect(addr)
        print(f"  TCP Connection to {name} succeeded!")
        context = ssl.create_default_context()
        ss = context.wrap_socket(s, server_hostname="discord.com")
        print(f"  TLS Handshake with {name} succeeded!")
        ss.close()
    except Exception as e:
        print(f"  Connection to {name} failed: {type(e).__name__} - {e}")

try:
    test_connection(socket.AF_INET, "IPv4")
except Exception as e:
    print("IPv4 test runner error:", e)

try:
    test_connection(socket.AF_INET6, "IPv6")
except Exception as e:
    print("IPv6 test runner error:", e)
print("=== DIAGNOSTIC CHECKS COMPLETE ===")

bot = commands.InteractionBot(reload=True, command_sync_flags=sync)

# Override login to instantiate the connector inside the active event loop
original_login = bot.login
async def custom_login(token: str):
    if bot.http.connector is None:
        bot.http.connector = aiohttp.TCPConnector(family=socket.AF_INET, force_close=True)
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
