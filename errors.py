# -*- coding: utf-8 -*-
from typing import Dict, Text
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse

KNOWN_API_ERRORS: Dict = {
    "ratelimited": "Превышен лимит запросов к API :("
}


class ApiError(BaseException):
    error: Text = None
    message: Text = "Неизвестная ошибка API :("

    def __init__(self, api_error: SlackApiError):
        self.error = api_error.response["error"]
        self.message = KNOWN_API_ERRORS.get(self.error, self.message)

    def handle(self, client: WebClient, data: Dict) -> SlackResponse:
        client.chat_postMessage(text=self.message, **data)
