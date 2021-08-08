import discord
from discord.ext import commands
from pathlib import Path

intents = discord.Intents.default()
intents.members = True

BOT_PREFIX = ('sudo ')
bot = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)


@bot.event
async def on_ready():
	print ("\nLogged in as:\t" + str(bot.user))
	print ("-----------------")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		embed = discord.Embed(description=f"○ Invalid command\n○ Type `sudo help` to know about each command.",colour=discord.Colour.light_gray())
		await ctx.send(embed = embed)
		return
if __name__ == '__main__':
	res = Path("res")

	with open(res / "TOKEN", 'r') as TokenObj:
		TOKEN = TokenObj.read()

	cogs = [
		'cogs.admin.mod',
		'cogs.admin.random'
	]

	for cog in cogs:
		print ("Loading Cog:\t", cog, "...")
		bot.load_extension(cog)

	bot.run(TOKEN)