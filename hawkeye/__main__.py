import os

from hawkeye.core.bot import Hawkeye

bot = Hawkeye()

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    bot.run()