from discord.ext import commands

from pathlib import Path

BOT_PREFIX = ('sudo ')
bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
	print ("\nLogged in as:\t" + str(bot.user))
	print ("-----------------")


if __name__ == '__main__':
	res = Path("res")

	with open(res / "TOKEN", 'r') as TokenObj:
		TOKEN = TokenObj.read()

	cogs = [
		'cogs.admin.template',
		'cogs.random.template'
	]

	for cog in cogs:
		print ("Loading Cog:\t", cog, "...")

		bot.load_extension(cog)


	bot.run(TOKEN)