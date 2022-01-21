import hikari
import lightbulb

from hawkeye.core.bot import Hawkeye
# from hawkeye.core.utils.Activity import Activity

admin_test= lightbulb.Plugin("admin_test", description="Handles Admin Plugins")
admin_test.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)

## Ping
@lightbulb.command("ping", "Shares bot latency.")
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")


## Echoes
@admin_test.command
@lightbulb.option("text", "Repeats your message.", required = True, modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("echo", "Echoesss.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(admin_test)
    
