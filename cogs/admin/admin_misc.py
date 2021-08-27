from asyncio.tasks import ensure_future
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import uuid
import datetime
import asyncio
import os
import os.path
from os import path

class admin_misc(commands.Cog):
	
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

	@commands.command(help = "Sends message anonymously  | sudo echo YourMessage ")
	@has_permissions(administrator=True)
	async def echo(self, ctx, *message):
		await ctx.message.delete()
		message = list(message)
		if message[0] == "--raw" or message[0] == "-r":
			await ctx.channel.send(" ".join(message[1:]))
			return
		message = " ".join(message)
		embed = discord.Embed(description=f"{message}",colour=discord.Colour.orange())
		await ctx.channel.send(embed = embed)

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
			await ctx.channel.send(embed = embed)
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
						await ctx.channel.send('%s' % user_id)
				else:
					if arg[len(arg)-1].isdigit():
						num = int(arg[len(arg) - 1])
						flag = True
					if int(num) != 69:
						if int(num) > 9:
							num = 9
						if str(num).isdigit():
							for i in range(int(num)):
								await ctx.channel.send('%s' % user_id)
						else:
							await ctx.channel.send("Give me a number.")
					else:
						await ctx.channel.send('%s' % user_id)
						emb = discord.Embed(title = "NICE!")
						await ctx.channel.send(embed = emb)
			except Exception as e:
				try:
					user = await self.bot.fetch_user(user_ID)
					embed = discord.Embed(description=f"{user} is not in the server.", colour=discord.Colour.red())
					await ctx.channel.send(embed = embed)
				except:
					
					if id.isdigit() and index == len(arg) - 1:
						pass
					else:
						embed = discord.Embed(description=f"Invalid user input.", colour=discord.Colour.red())
						await ctx.channel.send(embed = embed)
	@superping.error
	async def superping_error(self, ctx, error):
		await ctx.channel.send(error)

def setup(bot):
	bot.add_cog(admin_misc(bot))