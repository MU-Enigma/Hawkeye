import discord
from discord.ext import commands

class info(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	@commands.command(help = "Shows the server details   | sudo serverinfo")
	async def serverinfo(self,ctx):
		try:
			role_number = len(ctx.guild.roles)
			
			bots_list= [bot.mention for bot in ctx.guild.members if bot.bot]
			total_text_channels = len(ctx.guild.text_channels)
			total_voice_channels = len(ctx.guild.voice_channels)

			admin_roles = [role for role in ctx.guild.roles if role.permissions.administrator]
			members = []
			a = []
			for role in admin_roles:
				for member in role.members:
					if member not in members and not member.bot:
						for i in range(0,3):
							a=[]
							for j in range(0,3):
								if member not in a and member not in members:
									a.append(member)
					if len(a)!=0:
						members.append(a)
			members = [m for m in members if members.count(m) == 1]
			s = [[str(e) for e in row] for row in members]
			lens = [max(map(len, col)) for col in zip(*s)]
			fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
			table = [fmt.format(*row) for row in s]
			print(table)
			admin_list_formatted = ""
			for i in range(len(table)):
				if i%3 == 0:
					admin_list_formatted+="\n"
				admin_list_formatted+=f"{table[i]}\t"

			serverinfoEmbed= discord.Embed(title='Server Information')
	
			serverinfoEmbed = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color.light_gray())
			serverinfoEmbed.set_thumbnail(url=ctx.guild.icon_url)
			serverinfoEmbed.add_field(name='Name', value=f"{ctx.guild.name}", inline=True)
			serverinfoEmbed.add_field(name='Server Description', value=ctx.guild.description, inline=True)
			serverinfoEmbed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
			serverinfoEmbed.add_field(name='Member Count', value=ctx.guild.member_count, inline=True)
			serverinfoEmbed.add_field(name='Channel Count', value=total_text_channels, inline=True)
			serverinfoEmbed.add_field(name='Voice Channels', value=total_voice_channels, inline=True)
			serverinfoEmbed.add_field(name='Highest Role', value=ctx.guild.roles[-1], inline=True)
			serverinfoEmbed.add_field(name='Bots', value=', '.join(bots_list), inline=True)
			serverinfoEmbed.add_field(name='Admin list', value=" | ".join(table), inline=False)
			
			await ctx.send(embed = serverinfoEmbed)
		except Exception as e:
			print(e)


def setup(bot):
	bot.add_cog(info(bot))