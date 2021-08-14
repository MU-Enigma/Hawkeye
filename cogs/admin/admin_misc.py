import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class admin_misc(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	@commands.command(help = "Sends message anonymously  | sudo echo YourMessage ")
	@has_permissions(administrator=True)
	async def echo(self, ctx, *, message):
		await ctx.message.delete()
		embed = discord.Embed(description=f"{message}",colour=discord.Colour.orange())
		await ctx.send(embed = embed)

	@echo.error
	async def echo_error(self,ctx, error):
		embed = discord.Embed(description=f"○ No message entered.\n○ Try typing something after echo -> `sudo echo YourMessage`.\n○ Type `sudo help` to know more about each command.",colour=discord.Colour.red())
		await ctx.channel.send(embed = embed)
	
	@commands.command(help = "SUPERPINGS PEOPLE! VERY RISKY")
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
def setup(bot):
	bot.add_cog(admin_misc(bot))