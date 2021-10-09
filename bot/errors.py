# -*- coding: utf-8 -*-
from typing import Dict, Text
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

KNOWN_API_ERRORS: Dict = {
    "ratelimited": "Превышен лимит запросов к API :("
}


class ApiError(Exception):
    error: Text = None
    message: Text = "Неизвестная ошибка API :("

    def __init__(self, api_error: SlackApiError, client: WebClient, data: Dict):
        self.error = api_error.response["error"]
        self.message = KNOWN_API_ERRORS.get(self.error, self.message)

        client.chat_postMessage(text=self.message, **data)

    def __str__(self):
        return f"{self.error}: {self.message}"
