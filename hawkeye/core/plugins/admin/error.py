import logging

import hikari
import lightbulb
from lightbulb import plugins
from hawkeye.core.bot import Hawkeye

errorPlugin = lightbulb.Plugin("error")

@errorPlugin.command
@plugins.listener()
async def on_error(self, event: hikari.ExceptionEvent) -> None:
    logging.error("An error has occured.")

async def on_command_error(self, event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.errors.CommandNotFound):
        return None

    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond(
            "There are some missing arguments: " + ", ".join(event.exception.missing_options)
        )

    if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        return await event.context.respond(f"Command is on cooldown. Try again in {event.exception.retry_after:.0f} seconds.")

    if isinstance(event.exception, lightbulb.errors.CommandInvocationError):
        raise event.exception.original

    await event.context.respond("An error has occured. Reponses not found.")
    raise event.exception

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errorPlugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(errorPlugin)