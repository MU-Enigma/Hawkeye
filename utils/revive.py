from asyncio.tasks import ensure_future
from discord.ext import commands
import json

class revive(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		self.tasks = []

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		try:
			with open("res/events.json", "rt") as file:
				data = json.load(file)
				for guild in self.bot.guilds:
					for channel in guild.text_channels:
						if channel.name == "announcements":
							for i in data:
								await self.schedule_events(channel, i, data[i]["date"], data[i]["time"], data[i]["topic"])
							break
		except:
			data = {}
			for guild in self.bot.guilds:
				for channel in guild.text_channels:
					if channel.name == "announcements":
						for i in data:
							await self.schedule_events(channel, i, data[i]["date"], data[i]["time"], data[i]["topic"])
						break
def setup(bot):
	bot.add_cog(revive(bot))