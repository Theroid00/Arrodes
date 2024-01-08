
import Lotm
from disnake.ext import commands 
from disnake import Intents
intents = Intents.default()
intents.members = True
intents.message_content = True
sync = commands.CommandSyncFlags()
sync.all()


bot = commands.InteractionBot(reload=True, command_sync_flags=sync)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.slash_command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')

@bot.slash_command(name = "aliases")
async def Aliases(ctx , name):
    await ctx.send("\n".join(Lotm.aliases(name)))

@bot.slash_command(name = "pathways")
async def Pathway(ctx , name):
    await ctx.send("\n".join(Lotm.pathways(name)))

@bot.slash_command(name = "authorities")
async def Authority(ctx , name):
    await ctx.send("\n".join(Lotm.authorities(name)))
bot.run('MTE4OTYzMzU3MzYxMTkxMzMyOA.G8ZNS-.29d55PcRR7WZB4Y2ihAbSDXxmXhOX-JqEUShRw')


