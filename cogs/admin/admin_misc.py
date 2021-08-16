from asyncio.tasks import ensure_future
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import uuid
import datetime
import asyncio
import os

class admin_misc(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		self.tasks = []

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				if channel.name == "announcements":
					try:
						with open("assets/events.json", "rt") as file:
							data = json.load(file)
					except:
						data = {}
					for i in data:
						await self.schedule_events(channel, i, data[i]["date"], data[i]["time"], data[i]["topic"])
					break



	@commands.command(help = "Sends message anonymously  | sudo echo YourMessage ")
	@has_permissions(administrator=True)
	async def echo(self, ctx, *message):
		await ctx.message.delete()
		message = list(message)
		if message[0] == "--raw" or message[0] == "-r":
			await ctx.send(" ".join(message[1:]))
			return
		message = " ".join(message)
		embed = discord.Embed(description=f"{message}",colour=discord.Colour.orange())
		await ctx.send(embed = embed)

	@echo.error
	async def echo_error(self,ctx, error):
		if isinstance(error, commands.MissingPermissions):
			pass
		else:
			embed = discord.Embed(description=f"○ No message entered.\n○ Try typing something after echo -> `sudo echo YourMessage`.\n○ Type `sudo help` to know more about each command.",colour=discord.Colour.red())
			await ctx.channel.send(embed = embed)
	
	@commands.command(help = "SUPERPINGS PEOPLE! VERY RISKY")
	@has_permissions(administrator=True)
	async def superping(self,ctx,*arg):
		if str(arg) == '()' or (len(arg) == 1 and arg[0].isdigit()) :
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning the user -> `sudo superping @User`.\n○ Type `sudo help` to know about each command.",colour=discord.Colour.red())
			await ctx.send(embed = embed)
			return
		extra_Users = arg
		index = 0
		for i in range(len(extra_Users)):
			id = extra_Users[i]
			index = i
			flag = False
			user_ID = id.replace("<@", "")
			user_ID = user_ID.replace(">", "")
			try:
				if arg[len(arg)-1].isdigit():
					num = int(arg[len(arg) - 1])
					flag = True
				member = await ctx.guild.fetch_member(int(str(user_ID.replace("!", ""))))
				user_id = id
				num = 2
				if len(arg) == 1:
					for i in range(2):
						await ctx.send('%s' % user_id)
				else:
					if arg[len(arg)-1].isdigit():
						num = int(arg[len(arg) - 1])
						flag = True
					if int(num) != 69:
						if int(num) > 9:
							num = 9
						if str(num).isdigit():
							for i in range(int(num)):
								await ctx.send('%s' % user_id)
						else:
							await ctx.send("Give me a number")
					else:
						await ctx.send('%s' % user_id)
						emb = discord.Embed(title = "NICE!")
						await ctx.send(embed = emb)
			except Exception as e:
				try:
					user = await self.bot.fetch_user(user_ID)
					embed = discord.Embed(description=f"{user} is not in the server.", colour=discord.Colour.red())
					await ctx.send(embed = embed)
				except:
					
					if id.isdigit() and index == len(arg) - 1:
						pass
					else:
						embed = discord.Embed(description=f"Invalid user input.", colour=discord.Colour.red())
						await ctx.send(embed = embed)



	@commands.command(pass_context = True ,help = " Adds Event    | sudo add_event dd-mm-yyyy hh:mm Topic")
	@has_permissions(administrator=True)
	async def add_event(self, ctx, date: str, time: str,*, topic):
		if len(topic) > 2000:
			await ctx.channel.send("I don't have Nitro unfortunately. Please type a message of length less than 2000 characters")
		dd , mm, yyyy = date.split('-')
		hh , minute = time.split(':')
		try:
			with open("assets/events.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}

		target_time = datetime.datetime.strptime(date,  "%d-%m-%Y").replace(hour = int(hh), minute = int(minute))
		current_time = datetime.datetime.utcnow() + datetime.timedelta(hours = 5 , minutes = 30)

		if(target_time < current_time):
			await ctx.channel.send("Time has already passed, I don't have a time machine unfortunately")
			return

		id = uuid.uuid1().hex
		data[id] = {
			"author" : str(ctx.message.author),
			"topic" : topic,
			"date" : date,
			"time" : time
		}
		with open("assets/events.json", "wt") as file:
			json.dump(data, file)
			await ctx.channel.send("An Event has been added")

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
					await channel.send(id+" " + topic)
				try:
					with open("assets/events.json", "rt") as file:
						data = json.load(file)
						del data[id]
				except:
					data = {}

				with open("assets/events.json", "wt") as file:
					json.dump(data, file)
			except asyncio.CancelledError:
				pass
		else:
			print("announcements channel not found")


	@commands.command(pass_context = True ,help = " Shows All Events    | sudo show_events")
	@has_permissions(administrator=True)
	async def show_events(self, ctx):
		await ctx.channel.send("YO")
		with open("assets/events.json", "rt") as file:
			data = json.load(file)
			if len(data) == 0:
				await ctx.channel.send("There are no events right now, `sudo add_event` to add events")
			else:
				await ctx.channel.send("There are "+ str(len(data)) + " event(s) right now")
				for i in data:
					embed = discord.Embed(description=f"ID : "+ str(i) + "\nTime : " +str(data[i]["time"]) + "\nAuthor : "+ data[i]["author"] + "\nEvent: "+ data[i]["topic"], colour=discord.Colour.dark_gold())
					await ctx.channel.send(embed = embed)

	@show_events.error
	async def show_events_error(self, ctx, error):
		await ctx.channel.send("There's no event to show, sudo add_event to add an event")



	@commands.command(pass_context = True ,help = " Adds Event    | sudo delete_event id")
	@has_permissions(administrator=True)
	async def delete_event(self, ctx, id:str):
		id = id.strip()
		try:
			with open("assets/events.json", "rt") as file:
				data = json.load(file)
		except:
			data = {}
		try:
			for task in self.tasks:
				if task[1] == id:
					self.tasks.remove(task)
					task[0].cancel()

			del data[id]
			with open("assets/events.json", "wt") as file:
				json.dump(data, file)
			await ctx.channel.send("The event with id {} has been deleted".format(id))
		except:
			await ctx.channel.send("ID not Valid !")


	@commands.command(pass_context = True ,help = " Delete All Events    | sudo delete_all_events")
	@has_permissions(administrator=True)
	async def delete_all_events(self, ctx):
		try:
			os.remove("assets/events.json")
			for task in self.tasks:
				self.tasks.remove(task)
				task[0].cancel()
			await ctx.channel.send("All events are deleted".format(id))
		except: 
			await ctx.channel.send("Something went wrong while removing events")


def setup(bot):
	bot.add_cog(admin_misc(bot))