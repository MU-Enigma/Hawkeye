import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class random(commands.Cog):
	
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

	@commands.command(pass_context = True ,help = "Purge messages             | sudo purge AnInteger", aliases = ("clear", "cls"))
	@has_permissions(administrator=True)
	async def purge(self, ctx, limit: int):
		await ctx.channel.purge(limit = limit+1)

	@purge.error
	async def purge_error(self,ctx, error):
		count = 0
		try:
			id = int(ctx.message.reference.message_id)
			msg = await ctx.fetch_message(id)
			if id is not None and msg is not None:
				async for m in ctx.channel.history(limit = None, oldest_first = False):
					if m.id == id:
						count+=1
						break
					else:
						count+=1
				await ctx.channel.purge(limit = count)
			else:
				embed = discord.Embed(description="Hey! something went wrong",colour=discord.Colour.red())
				await ctx.channel.send(embed = embed)
		except:
			embed = discord.Embed(description=f"○ A parameter is missing.\n○ Try mentioning one integer -> `sudo purge Number`.\n○ Or else reply to a message and type -> `sudo purge` .\n○ Type `sudo help` to know more about each command.",colour=discord.Colour.red())
			await ctx.channel.send(embed = embed)




	@commands.command(pass_context = True ,help = "Purge messages of @user    | sudo purge_user @mention AnInteger", aliases = ("clear_user", "cls_user"))
	@has_permissions(administrator=True)
	async def purge_user(self, ctx, member:discord.Member, limit: int):
		def is_member(m):
			return m.author == member

		await ctx.channel.purge(limit = limit+1, check = is_member)
		await ctx.channel.send(member.mention+", Your messages have been deleted")
		
	@purge_user.error
	async def purge_user_error(self,ctx, error):
		embed = discord.Embed(description=f"○ Missing Parameter(s).\n○ Try mentioning user and provide an integer -> `sudo purge_user @user Number`.\n○ Type `sudo help` to know more  about each command.",colour=discord.Colour.red())
		await ctx.channel.send(embed = embed)


def setup(bot):
	bot.add_cog(random(bot))