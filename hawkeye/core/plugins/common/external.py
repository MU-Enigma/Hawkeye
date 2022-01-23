import lightbulb

externalPlugin = lightbulb.Plugin("External")

##Hawkye Github repo
@externalPlugin.command
@lightbulb.command("src", "Returns main Hawkeye repo.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def src(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/Hawkeye>")
async def src(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/Hawkeye>")

##Enigma Github
@externalPlugin.command
@lightbulb.command("git", "Returns the Enigma Github")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def src(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/>")
async def src(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"<https://github.com/MU-Enigma/>")

##Enigma website
@externalPlugin.command
@lightbulb.command("website", "Returns the Enigma website")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def src(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"<https://mu-enigma.github.io/>")
async def src(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"<https://mu-enigma.github.io/>")

##Google search
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

##DuckDuckGo search
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

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(externalPlugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(externalPlugin)