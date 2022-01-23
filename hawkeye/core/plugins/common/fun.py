from random import random
import requests
import json
import hikari
import lightbulb
import requests
from lightbulb import commands
from hikari.colors import Color
import random

funPlugin = lightbulb.Plugin("fun")

## 8ball
@funPlugin.command
@lightbulb.set_help("Give answers to your questions.")
@lightbulb.option("question", "The question you want answers to.")
@lightbulb.command("8ball", description="Make the game of the 8ball.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_ball(ctx: lightbulb.SlashContext):
    
    responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."]


    await ctx.respond(f"{random.choice(responses)}")

## Give cookie
@funPlugin.command
@lightbulb.set_help("Give a cookie (1 hour cooldown).")
@lightbulb.add_cooldown(length=3600, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "User you want give the cookie", hikari.Member)
@lightbulb.command(name="givecookie", aliases=("gcookie",), description="Give a cookie to a user.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_cookie(ctx: lightbulb.SlashContext) -> None:

    target = ctx.options.user

    if target.id == ctx.member.id:
        await ctx.respond("You can't give a cookie to yourself.")
        return

    if target.is_bot:
        await ctx.respond("You can't give cookies to bots.")
        return

    await funPlugin.bot.d.db.execute(
         "UPDATE user SET cookies = cookies + 1 WHERE user_id = ?", 
          target.id
        )
   
    row = await ctx.bot.d.db.try_fetch_record(
        "SELECT cookies FROM user WHERE user_id = ?",
        target.id,
    )

    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    images_cookies = ["https://i.pinimg.com/originals/fc/39/65/fc3965c433c19f4492d616f975316c8c.gif", "https://64.media.tumblr.com/2f272878761f85dbe7665c1fada53e45/c0f2b8287c49f60d-4b/s540x810/aecab8278a4762d638af1a6dcda55e16c069c458.gif", "https://c.tenor.com/zEWVjcnOt1IAAAAC/anime-eating.gif", "https://c.tenor.com/bBRCCeAYPU8AAAAC/cookie-mashiro.gif"]

    embed = (hikari.Embed(
        description=f"You gave a cookie to **{target.username}**, now he/she has **{row.cookies}**",
        colour=Color.from_rgb(r_g, r_b, r_r)

    )
    .set_image(random.choice(images_cookies))
    )

    await ctx.respond(embed)

## Anime gifs
def get_gif(term, limit = 14) -> str:
    with open("./secrets/api-tenor", "r") as f:
        api_key = f.readline()
    limit = limit
    
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (term, api_key, limit))


    gifs_data = json.loads(r.content)
    gif = gifs_data["results"][random.randint(0,limit-1)]["media"][0]["gif"]["url"]

    return 

async def action(ctx: lightbulb.Context, text, image) -> None:
    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    embed = (hikari.Embed(
        description=f"{text}",
        colour=Color.from_rgb(r_g, r_b, r_r)
    )
    .set_image(image)
    )

    await ctx.respond(embed)


## Hugs person mentioned
@funPlugin.command
@lightbulb.set_help("Give a hug to whoever mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("hug", "Just hug someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_hug(ctx: lightbulb.context) -> None:
    target = ctx.options.member
    gif = get_gif("anime-hug")

    await action(ctx, f"**{ctx.member.username}** hug to **{target.username}**", gif)

## Claps for person mentioned
@funPlugin.command
@lightbulb.set_help("Clap or clap for someone.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("clap", "Just clap or clap for someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_clap(ctx: lightbulb.context) -> None:
    
    target = ctx.options.member

    gif = get_gif("anime-clap")

    if target == None:
        await action(ctx, f"**{ctx.member.username}** is clapping", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** applauds **{target.username}**", gif)

## High fives person mentioned
@funPlugin.command
@lightbulb.set_help("Highfive to the person who mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("highfive", "Highfive to someone :)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_highfive(ctx: lightbulb.context) -> None:
    
    target = ctx.options.member

    gif = get_gif("anime-highfive")
    await action(ctx, f"**{ctx.member.username}** highfive to **{target.username}**", gif)

## Laugh at someone mentioned
@funPlugin.command
@lightbulb.set_help("Laugh or tease someone you mention")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("laugh", "Laugh or tease.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_laugh(ctx: lightbulb.context) -> None:
    
    target = ctx.options.member

    gif = get_gif("anime-laugh")
    if target == None:
        await action(ctx, f"**{ctx.member.username}** is laughing.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** laughs at **{target.username}**", gif)

## Kiss the person mentioned
@funPlugin.command
@lightbulb.set_help("Kiss the person who mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("kiss", "Kiss someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_kiss(ctx: lightbulb.context) -> None:
    target = ctx.options.member
    if target.id == ctx.member.id:
        await ctx.respond(f"I don't think you can kiss yourself {ctx.member.mention}")
        return

    gif = get_gif("anime-kiss")
    await action(ctx, f"**{ctx.member.username}** le dio un beso a **{target.username}**. (づ￣ ³￣)づ", gif)

## Code grind
@funPlugin.command
@lightbulb.set_help("Show you are changing the world whit code.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("grind", "Programming alone or with someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_program(ctx: lightbulb.context) -> None:
    target = ctx.options.member
    gif = get_gif("anime-programmer", limit=3)

    if target == None:
        await action(ctx, f"**{ctx.member.username}** is programming something amazing.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** is programming something amazing with **{target.username}**", gif)

## Converts celsius to farenheit and vice versa
@funPlugin.command
@lightbulb.option('fahrenheit', 'Temperature in Fahrenheit to convert.', required=True, type=float)
@lightbulb.command('celsius', 'Convert Fahrenheit to Celsius.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def celsius_command(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(
        embed=hikari.Embed(
            title='Fahrenheit to Celsius',
            description=f'({ctx.options.fahrenheit} - 32) * (5/9) = **{((int(ctx.options.fahrenheit) - 32) * (5/9)):.1f}**',
            color=hikari.Color(0x289C9C)
        )
    )

@funPlugin.command
@lightbulb.option('celsius', 'Temperature in Celsius to convert.', required=True, type=float)
@lightbulb.command('fahrenheit', 'Convert Celsius to Fahrenheit.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def fahrenheit_command(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(
        embed=hikari.Embed(
            title='Celsius to Fahrenheit',
            description=f'{ctx.options.celsius} * (9/5) + 32 = **{(int(ctx.options.celsius) * (9/5) + 32):.1f}**',
            color=hikari.Color(0x289C9C)
        )
    )

## Rolls dice
@funPlugin.command
@lightbulb.option("bonus", "A fixed number to add to the total roll.", int, default=0)
@lightbulb.option("sides", "The number of sides each die will have.", int, default=6)
@lightbulb.option("number", "The number of dice to roll.", int)
@lightbulb.command("dice", "Roll one or more dice.")
@lightbulb.implements(commands.SlashCommand)
async def dice(ctx: lightbulb.context.Context) -> None:
    number = ctx.options.number
    sides = ctx.options.sides
    bonus = ctx.options.bonus

    if number > 25:
        await ctx.respond("No more than 25 dice can be rolled at once.")
        return

    if sides > 100:
        await ctx.respond("The dice cannot have more than 100 sides.")
        return

    rolls = [random.randint(1, sides) for _ in range(number)]
    await ctx.respond(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )