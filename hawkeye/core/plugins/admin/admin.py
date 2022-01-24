from bisect import insort_right
import logging
import hikari
import lightbulb

from hawkeye.core.bot import Hawkeye
# from hawkeye.core.utils.Activity import Activity

adminPlugin= lightbulb.Plugin("admin", description="Handles Admin Plugins")
adminPlugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)

## Ping
@adminPlugin.command
@lightbulb.command("ping", "Shares bot latency.")
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")

## Shutdown
@adminPlugin.command
@lightbulb.command("shutdown", "Shuts down the bot.")
async def shutdown(ctx: lightbulb.Context) -> None:
    await ctx.bot.close(force=False)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(adminPlugin)
    
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(adminPlugin)