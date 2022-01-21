from ast import alias
from random import random
from smtplib import _Reply
import hikari
import lightbulb
import random
from datetime import datetime

funPlugin = lightbulb.Plugin("fun")

##Greets member
@funPlugin.command
@lightbulb.command("hello", aliases=("hi", "hey"))
async def hello(ctx: lightbulb.Context) -> None:
    greeting = random.choice(("Hello", "Hi", "Hey", "Hey there", "Hello there"))
    await ctx.respond(f"{greeting}!", reply=True, mentions_reply=True,)

##Rolls dice (in progress)
@funPlugin.command
@lightbulb.command("dice", aliases="roll, ")
async def dice(ctx: lightbulb.Context, dice: str) -> None:
    number, highest = (int(term) for term in dice.split("d"))

    if number > 25:
        return await ctx.respond("I can only roll upto 25 dice at one time.")

    rolls = [random.randint(1, highest) for i in range(number)]
    await ctx.respond("+".join(str(r) for r in rolls) + (f" = {sum(rolls):, }"), reply=True, mentions_reply=True,)