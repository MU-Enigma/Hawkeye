import discord
from discord.ext import commands

class src(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	@commands.command(help = "Returns the Github link   | sudo git")
	async def git(ctx) :
		gitembed= discord.Embed(title='')

		gitembed.add_field(name='Github Link',value="https://github.com/MU-Enigma",inline=True)
	
		await ctx.send(embed=gitembed)


	@commands.command(help = "Returns the Hawkeye Repo link   | sudo git")
	async def src(ctx) :
		srcembed= discord.Embed(title='')

		srcembed.add_field(name='Hawkeye Repository',value="https://github.com/MU-Enigma/Hawkeye",inline=True)
	
		await ctx.send(embed=srcembed)

def setup(bot):
	bot.add_cog(src(bot))