import hikari
from itertools import cycle
import asyncio


class Activity:
    """
    Custom class that changes the Bot's Rich Presence
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.presence = cycle(
            [
                hikari.Activity(type=hikari.ActivityType.WATCHING, name="Devs Code"),
                hikari.Activity(type=hikari.ActivityType.COMPETING, name = "Time"),
                hikari.Activity(type=hikari.ActivityType.LISTENING, name="Developers"),
                hikari.Activity(type=hikari.ActivityType.PLAYING, name = "Code"),
                # hikari.Activity(type=hikari.ActivityType.STREAMING, name="Nothing"),

            ]
        )


    async def change_status(self) -> None:
        while True:
            new_presence = next(self.presence)
            await self.bot.update_presence(
                activity=new_presence, status=hikari.Status.ONLINE
            )
            await asyncio.sleep(10) ## Changes presence every 10 seconds
    