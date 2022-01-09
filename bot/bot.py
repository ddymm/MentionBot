# -*- coding: utf-8 -*-
from typing import Dict, List, Text
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse
from .errors import ApiError


class MentionBot(object):
    def __init__(self, client: WebClient, body: Dict):
        self.client = client

        event: Dict = body["event"]
        self.data: Dict = {
            "thread_ts": event.get(
                "thread_ts", event["event_ts"]
            ),  # Хак, чтобы меншны работали и из каналов, и из тредов.
            "channel": event["channel"],
        }

    def send_message(self, text: Text) -> SlackResponse:
        # Отправка сообщения-ответа от бота.
        return self.client.chat_postMessage(text=text, **self.data)

    def get_data_from_message(self, event: Dict) -> (List[Text], List[Text]):
        # Достаём список id заменшненых групп и список id пользователей из ивента-упоминания бота.

        user_ids: List[Text] = [
            obj["user_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "user"
        ]
        group_ids: List[Text] = [
            obj["usergroup_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "usergroup"
        ]

        user_ids, group_ids = list(set(user_ids)), list(set(group_ids))

        if not group_ids and len(user_ids) == 1:  # когда заменшнен только бот.
            self.send_message(text="Некорректный запрос.")

        else:
            self.send_message(text="Собираю данные...")

        return user_ids, group_ids

    def get_users_list_from_group(self, group_id: Text) -> List[Text]:
        # Достаём список id пользователей из группы.

        try:
            users_list_response_data: SlackResponse = self.client.usergroups_users_list(usergroup=group_id)
        except SlackApiError as api_error:  # Переоборачиваем ошибку API, что б послать читаемый ответ от бота.
            raise ApiError(api_error, self.client, self.data)

        return users_list_response_data["users"]

    def get_email_from_user(self, user_id: Text) -> Text:
        # Достаём поле email из профиля пользователя.

        try:
            user_info_response_data: SlackResponse = self.client.users_info(user=user_id)
        except SlackApiError as api_error:  # Переоборачиваем ошибку API, что б послать читаемый ответ от бота.
            raise ApiError(api_error, self.client, self.data)

        if not user_info_response_data["user"]["is_bot"]:
            return user_info_response_data["user"]["profile"]["email"]
