import discord 
from discord.ext import commands

class messageHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('random_test')
	async def tester(self, ctx):
		print("In the command")
		await ctx.channel.send('Good news {}! Random are working just fine'.format(ctx.message.author.mention))

def setup(bot):
	bot.add_cog(messageHandler(bot))