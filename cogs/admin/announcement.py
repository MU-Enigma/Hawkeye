from asyncio.tasks import ensure_future
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import shortuuid
import datetime
import asyncio
import os


class announcement(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		self.tasks = []

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		try:
			with open("res/data.json", "rt") as file:
				data = json.load(file)
				for guild in self.bot.guilds:
					for channel in guild.text_channels:
						if channel.name == "announcements":
							for i in data:
								await self.schedule_events(channel, i, data['events'][i]["date"], data['events'][i]["time"], data['events'][i]["topic"])
							break
		except:
			data = {}
			for guild in self.bot.guilds:
				for channel in guild.text_channels:
					if channel.name == "announcements":
						for i in data:
							await self.schedule_events(channel, i, data['events'][i]["date"], data['events'][i]["time"], data['events'][i]["topic"])
						break

	@commands.command(pass_context = True ,help = " Adds Event    | sudo add_event dd-mm-yyyy hh:mm Topic", aliases = ["add-event", "event", "announce"])
	@has_permissions(administrator=True)
	async def add_event(self, ctx, date: str, time: str,*, topic):
		if len(topic) > 2000:
			await ctx.channel.send("I don't have Nitro unfortunately. Please type a message of length less than 2000 characters.")
		dd , mm, yyyy = date.split('-')
		hh , minute = time.split(':')
		try:
			with open("res/data.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}

		target_time = datetime.datetime.strptime(date,  "%d-%m-%Y").replace(hour = int(hh), minute = int(minute))
		current_time = datetime.datetime.utcnow() + datetime.timedelta(hours = 5 , minutes = 30)

		if(target_time < current_time):
			await ctx.channel.send("Time has already passed, I don't have a time machine unfortunately.")
			return

		id = shortuuid.uuid().hex
		if not 'events' in data:
			data["events"] = {}
		data["events"][id] = {
			"author" : str(ctx.message.author),
			"topic" : topic,
			"date" : date,
			"time" : time
		}
		with open("res/data.json", "wt") as file:
			json.dump(data, file)
			embed = discord.Embed(description = "An Event has been added.", colour=discord.Colour.light_gray())
			await ctx.channel.send(embed = embed)
			

		await self.schedule_events(discord.utils.get(ctx.guild.text_channels, name = "announcements"), id, date, time, topic)

	@add_event.error
	async def add_event_error(self, ctx, error):
		embed = discord.Embed(description=f"○ Invalid Parameter(s).\n○ Try sticking to this format -> `sudo add_event dd-mm-yyyy hh:mm`.\n○ Type `sudo help` to know more  about each command.",colour=discord.Colour.red())
		await ctx.channel.send(error, embed = embed)

	async def schedule_events(self, channel, id, date, time, topic):
		hh , minute = time.split(':')
		hh = int(hh)
		minute = int(minute)
		target_time = datetime.datetime.strptime(date,  "%d-%m-%Y").replace(hour = hh, minute = minute)
		current_time = datetime.datetime.utcnow() + datetime.timedelta(hours = 5 , minutes = 30)
		delta = (target_time - current_time).total_seconds()
		asyncio.create_task(self.send_message_scheduler(channel, id, delta, topic))


	async def send_message_scheduler(self, channel, id, delta , topic):
		if channel:
			task = asyncio.create_task(asyncio.sleep(delta))
			self.tasks.append([task, id])
			try:
				await task
				self.tasks.remove([task, id])
				if delta >= 0:
					await channel.send(topic)
				try:
					with open("res/data.json", "rt") as file:
						data = json.load(file)
						del data["events"][id]
				except:
					data = {}

				with open("res/data.json", "wt") as file:
					json.dump(data, file)
			except asyncio.CancelledError:
				pass
		else:
			print("announcements channel not found!")
			

	@commands.command(pass_context = True ,help = " Shows All Announcements Scheduled    | sudo events", aliases = ["events-ls", "show_events", "announcements"])
	@has_permissions(administrator=True)
	async def events(self, ctx):
		
		with open("res/data.json", "rt") as file:
			data = json.load(file)
			if not "events" in data:
				data["events"] = {}
			if len(data["events"]) == 0:
				embed = discord.Embed(description="There are no announcements scheduled, `sudo add_event` to add events.", colour=discord.Colour.light_gray())
				await ctx.channel.send(embed = embed)
				return
			else:
				if len(data["events"]) > 1:
					embed = discord.Embed(title = f"There are {len(data['events'])} announcements scheduled.", colour = discord.Colour.gold())
				else:
					embed = discord.Embed(title = f"There is {len(data['events'])} announcement scheduled.", colour = discord.Colour.gold())
				count = 1
				for i in data["events"]:
					embed.add_field(name = f"{count}) {str(data['events'][i]['date'])}", value = f"Event : {data['events'][i]['topic']}\nAuthor : {data['events'][i]['author']}\nTime : {str(data['events'][i]['time'])}\nID : {str(i)}", inline = False)
					count+=1
				await ctx.channel.send(embed = embed)

	@events.error
	async def events_error(self, ctx, error):
		embed = discord.Embed(description="There are no announcements scheduled, sudo add_event to add an event.", colour=discord.Colour.light_gray())
		await ctx.channel.send(embed = embed)



	@commands.command(pass_context = True ,help = " Adds Event    | sudo delete_event id", aliases = ["remove-event, delete-event, kill-event"])
	@has_permissions(administrator=True)
	async def delete_event(self, ctx, id:str):
		id = id.strip()
		try:
			with open("res/data.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}
		try:
			for task in self.tasks:
				if task[1] == id:
					self.tasks.remove(task)
					task[0].cancel()

			del data["events"][id]
			with open("res/data.json", "wt") as file:
				json.dump(data, file)
			embed=discord.Embed(color=discord.Colour.dark_red(), title="Event Deleted", description = f"The announcement with ID: {id} has been removed.")
			await ctx.channel.send(embed = embed)
		except:
			embed = discord.Embed(description=f"Invalid Event ID! Try Again.", colour=discord.Colour.red())
			await ctx.channel.send(embed = embed)

	@commands.command(pass_context = True ,help = " Delete All Events    | sudo delete_all_events", aliases = ["remove-all-events", "delete-all-events"])
	@has_permissions(administrator=True)
	async def delete_all_events(self, ctx):
		try:
			os.remove("res/data.json")
			for task in self.tasks:
				self.tasks.remove(task)
				task[0].cancel()
			await ctx.channel.send()
			embed = discord.Embed(description = f"All the events have been cleared.", colour=discord.Colour.dark_red())
			await ctx.channel.send(embed = embed)
		except: 
			embed = discord.Embed(description = "Something went wrong while removing events.", colour=discord.Colour.red())
			await ctx.channel.send(embed = embed)

def setup(bot):
	bot.add_cog(announcement(bot))