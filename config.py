# -*- coding: utf-8 -*-
from pydantic import BaseSettings


class Configuration(BaseSettings):
    app_token: str
    bot_token: str

    class Config:
        env_file = ".env"


CONFIG = Configuration()
