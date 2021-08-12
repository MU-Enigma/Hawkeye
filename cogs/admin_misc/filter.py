import discord
from discord.ext import commands
from discord.member import Member
from discord.ext.commands import has_permissions
from discord import guild

nsfw_Words = ["fuck", "nigga", "cunt", "snork", "milf", "labe", "gangbang", "dick", "fuck yo mama", "fucker", "felcher", "chilf", "asshole"]
class nsfw(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_message(self, message):
		for word in nsfw_Words:
			if word in str(message.content).lower():
				await message.delete()
def setup(bot):
	bot.add_cog(nsfw(bot))