import hikari
from hikari import Color
import lightbulb
import wikipedia

import datetime as dt
from datetime import datetime, time, timedelta
from wikipedia import exceptions

from wikipedia.wikipedia import languages


externalPlugin = lightbulb.Plugin("External")

##Hawkye Github repo
@externalPlugin.command
@lightbulb.command("src", "Returns main Hawkeye repo.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def src(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/Hawkeye>")
async def src(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/Hawkeye>")

## Sends link to Enigma Github
@externalPlugin.command
@lightbulb.command("git", "Returns the Enigma Github")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def src(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/>")
async def src(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/>")

## Sends link to Enigma website
@externalPlugin.command
@lightbulb.command("website", "Returns the Enigma website")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def src(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"<https://mu-enigma.github.io/>")
async def src(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"<https://mu-enigma.github.io/>")

## Google search
@externalPlugin.command
@lightbulb.option("query", "The thing to search.")
@lightbulb.command("google", "Let me Google that for you...")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def google(ctx: lightbulb.Context) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://letmegooglethat.com/?q={q.replace(' ', '+')}>")

async def google(ctx: lightbulb.SlashContext) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://letmegooglethat.com/?q={q.replace(' ', '+')}>")

## DuckDuckGo search
@externalPlugin.command
@lightbulb.option("query", "The thing to search.")
@lightbulb.command("duckduckgo", "Let me Duck Duck Go that for you...")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def duckduckgo(ctx: lightbulb.Context) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://lmddgtfy.net/?q={q.replace(' ', '+')}>")

async def duckduckgo(ctx: lightbulb.SlashContext) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://lmddgtfy.net/?q={q.replace(' ', '+')}>")

## Wikipedia search
@externalPlugin.command()
@lightbulb.set_help("Search wikipedia.")
@lightbulb.option("query", "The thing to search.")
@lightbulb.command(name="wikipedia", aliases=("wiki","wk"), description="Search a target in wikipedia.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_wikipedia(ctx: lightbulb.SlashContext) -> None:
    try:
        message = await ctx.respond("Searching...")
        page = wikipedia.page(ctx.options.search)
        image = page.images[0]
        title = page.title
        content = page.content

        if len(content) > 600:
            content = content[:600] + "...(READ MORE click on the title)"

        else:
            content = content

        title_link = title.replace(" ", "_")
        embed = (hikari.Embed(
                colour=Color(0x3B9DFF),
                description=content,
                timestamp=dt.datetime.now().astimezone()

        )
        .set_image(image)
        .set_author(name=title,url=f"https://en.wikipedia.org/wiki/{title_link}")
        )
        await ctx.respond(embed, reply=True)
        await message.delete()

    except(wikipedia.exceptions.DisambiguationError):
        await message.edit(content="Try to be clearer with the search, multiple results found.")

    except(wikipedia.exceptions.PageError):
        await message.edit(content="Page not found.")

    except(wikipedia.exceptions.HTTPTimeoutError):
        await message.edit(content="The servers seem to be down. Please try again later.")

## Reddit search
@externalPlugin.command
@lightbulb.option("query", "The thing to search.")
@lightbulb.command("reddit", "Searching on Reddit.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def reddit(ctx: lightbulb.Context) -> None:
    q = ctx.options.query

    if len(q) > 50:
        await ctx.respond("Your query should be no longer than 50 characters.")
        return

    await ctx.respond(f"<https://www.reddit.com/search.json?q={q.replace(' ', '+')}>")

async def duckduckgo(ctx: lightbulb.SlashContext) -> None:
    q = ctx.options.query

    if len(q) > 50:
        await ctx.respond("Your query should be no longer than 50 characters.")
        return

    await ctx.respond(f"<https://www.reddit.com/search.json?q={q.replace(' ', '+')}>")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(externalPlugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(externalPlugin)