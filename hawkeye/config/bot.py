from typing import List
from pydantic import BaseSettings

class BotConfig(BaseSettings):
    token: str
    prefix: str
    test_guilds: List[int]

    class Config:
        env_file = ".env"
        env_prefix = "bot_"


bot_config = BotConfig()