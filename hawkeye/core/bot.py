import asyncio
from asyncio.subprocess import STDOUT
import hikari 
import lightbulb
from hawkeye.core.utils.Activity import Activity
from hawkeye import bot_config

HOME_GUILD_ID: 870647011899220040
STDOUT_CHANNEL_ID: 931779674118451230

class Hawkeye(lightbulb.BotApp):

    def __init__(self) -> None:
        super().__init__(
            token=bot_config.token,
            prefix=bot_config.prefix,
            default_enabled_guilds=bot_config.test_guilds,
            intents=hikari.Intents.ALL,
            banner = None,
            ignore_bots=True,
        )


    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.StoppedEvent, self.on_stopped)
        self.event_manager.subscribe(hikari.GuildMessageCreateEvent, self.on_message)
        # self.event_manager.subscribe(lightbulb.CommandErrorEvent, on_error)
        # self.event_manager.subscribe(hikari.ShardReadyEvent, self.on_shard_ready)

        super().run(asyncio_debug=True,
        coroutine_tracking_depth=20,    # enable tracking of coroutines, makes some asyncio
                                        # errors clearer.
        propagate_interrupts=True,)    # Any OS interrupts get rethrown as errors.


    async def on_starting(self, _: hikari.StartingEvent) -> None:
        print("Starting the Bot ... ")
        self.load_extensions_from("hawkeye/core/plugins/", must_exist=True, recursive=True)
        print("Plugins Loaded ...")

    async def on_started(self, _: hikari.StartedEvent) -> None:
        asyncio.create_task(Activity(self).change_status())
        print("Bot has started sucessfully.")

        self.home_guild = self.cache.get_guild(HOME_GUILD_ID)
        self.stdout_channel = self.home_guild.get_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"Testing... now online!")


    async def on_stopping(self, _: hikari.StoppingEvent) -> None:
        print("Bot is stopping...")

    async def on_stopped(self, _: hikari.StoppedEvent) -> None:
        print("Bot has stopped...")


    async def on_message(self, event: hikari.GuildMessageCreateEvent) -> None:
        if not event.is_human or not event.message.content:
            return

        if not f"<@!{self.get_me().id}>" == event.message.content.strip():
            return

        prefix = bot_config.prefix
        response = f"""
            Hi {event.author.mention}, My prefix here is `{prefix}`
            You can view the help using `{prefix}help`
            Thank you for using me.
            """

        await event.message.respond(
            embed=hikari.Embed(description=response, color=0x99CCFF).set_footer(
                text=f"Cheers from the Enigma's Team."
            )
        )