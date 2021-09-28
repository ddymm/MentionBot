# -*- coding: utf-8 -*-
from typing import Dict, Text

from slack_sdk import WebClient

KNOWN_API_ERRORS: Dict = {
    "ratelimited": "Превышен лимит запросов к API :("
}


class ApiError(Exception):
    message: Text = "Неизвестная ошибка API :("
    error: Text = None

    def __init__(self, api_error):
        self.error = api_error.response["error"]
        self.message = KNOWN_API_ERRORS.get(self.error, self.message)

    def handle(self, client, data):
        client.chat_postMessage(text=self.message, **data)
