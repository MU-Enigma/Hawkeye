import discord 
from discord.ext import commands
from discord.member import Member
from typing import Optional
from datetime import datetime
from discord.embeds import Embed
from discord.ext.commands import has_permissions, MissingPermissions

class messageHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('random_test')
	async def tester(self, ctx):
		print("In the command")
		await ctx.channel.send('Good news {}! Random are working just fine'.format(ctx.message.author.mention))
	
	@commands.command(name = "userinfo" , alias_flag_value = "ui")
	async def userinfo(self,ctx, target: Optional[Member]):
		target = target or ctx.author
		embed = Embed(title="User Information",
					colour = target.colour,
					timestamp = datetime.utcnow())
		fields = [("Name", str(target), True),
					("ID", target.id, True), 
					("Bot?", target.bot, True),
					("Top Role", target.top_role.mention, True),
					("Status", str(target.status).title(), True),
					# ("Activity", f"{str(target.activity.type).split('.')[-1].title()} {target.activity.name}", True),
					("Created on", target.created_at.strftime("%d/%m/%Y %H hrs/%M min/%S sec"), True),
					("Joined at", target.joined_at.strftime("%d/%m/%Y %H hrs/%M min/%S sec"), True),
					("Boosted", bool(target.premium_since), True)]
		for name, value, inline in fields:
			embed.add_field(name = name, value = value, inline = inline)
			
		embed.set_thumbnail(url = target.avatar_url)
		await ctx.send(embed = embed)
	@commands.command(help = "SUPERPINGS PEOPLE! VERY RISKY")
	async def superping(self,ctx,*arg):
		#print(f"this is arg: {arg}")
		user_id = '<@201909896357216256>'
		user_id = arg[0].replace("!","")
		num = 2
		if len(arg) == 1:
			for i in range(2):
				await ctx.send('%s' % user_id)
		else:
			num = int(arg[1])
			if int(num) > 9:
				num = 9
			#print(f"THIS IS TARGET: {target}")
			if str(num).isdigit():
				if int(num) == 69:
					await ctx.send('%s' % user_id)
					emb = discord.Embed(title = "NICE!")
					await ctx.send(embed = emb)
				else:
					for i in range(int(num)):
						await ctx.send('%s' % user_id)
			else:
				await ctx.send("Give me a number")

	@commands.command(help = "Creates a temporary server invite link and sends")
	@has_permissions(administrator = True)
	async def create_invite(self,ctx):
		"""Create instant invite"""
		link = await ctx.channel.create_invite(max_age = 300)
		await ctx.send(link)
def setup(bot):
	bot.add_cog(messageHandler(bot))