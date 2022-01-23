import hikari
import lightbulb
from lightbulb import commands, context
from datetime import datetime
from random import randint

infoPlugin = lightbulb.Plugin("info")

## Returns avatar of user
@infoPlugin.command
@lightbulb.option("target", description = "User to fetch avatar of", type = hikari.User, required = False)
@lightbulb.command("avatar", description = "Fetch Avatar of yourself or the specified user.", aliases = ['av', 'pfp'], auto_defer = True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def avatar_cmd(ctx: context.Context) -> None:
    target = ctx.options.target if ctx.options.target is not None else ctx.author

    embed = hikari.Embed(
		title = f"Avatar of {target.username}",
		color = randint(0, 0x3B9DFF)
	).set_image(
		target.avatar_url
	).set_footer(
		text = f"Requested by {ctx.author.username}",
		icon = ctx.author.avatar_url
	).set_author(
		name = f"{ctx.app.get_me().username}",
		icon = ctx.app.get_me().avatar_url
	)

    await ctx.respond(embed = embed, reply = True)

## Returns info about the user
@infoPlugin.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("userinfo", "Get info on a server member.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:

    target = ctx.get_guild().get_member(ctx.options.target or ctx.user)
    if not target:
        await ctx.respond("The mentioned user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone

    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x3B9DFF,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(target.avatar_url or target.default_avatar_url)
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            "Roles",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
    )

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(infoPlugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(infoPlugin)