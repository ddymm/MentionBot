# -*- coding: utf-8 -*-
from typing import Dict, List, Text, Union
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse
from errors import ApiError


class MentionBot(object):
    client: WebClient = None
    data: Dict = {}

    def __init__(self, client: WebClient, body: Dict):
        event: Dict = body["event"]
        data: Dict = {
            "thread_ts": event.get(
                "thread_ts", event["event_ts"]
            ),  # Хак, чтобы меншны работали и из каналов, и из тредов.
            "channel": event["channel"],
        }

        self.client = client
        self.data = data

    def send_message(self, text: Text) -> SlackResponse:
        return self.client.chat_postMessage(text=text, **self.data)

    def get_data_from_message(self, event: Dict) -> Dict:
        # Достаём списки заменшненых групп и пользователей из ивента-упоминания бота.

        mentioned_users: List = [
            obj["user_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "user"
        ]
        mentioned_groups: List = [
            obj["usergroup_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "usergroup"
        ]

        user_ids, group_ids = list(set(mentioned_users)), list(set(mentioned_groups))

        if not group_ids and len(user_ids) == 1:  # когда заменшнен только бот.
            self.send_message(text="Некорректный запрос.")

        else:
            self.send_message(text="Собираю данные...")

        return {"user_ids": user_ids, "group_ids": group_ids}

    def get_users_list_from_group(self, group_id: Text) -> Union[List[Text], SlackResponse]:
        # Достаём список пользователей из группы.

        try:
            users_list_response_data = self.client.usergroups_users_list(usergroup=group_id)
        except SlackApiError as api_error:
            raise ApiError(api_error).handle(self.client, self.data)

        return users_list_response_data["users"]

    def get_email_from_user(self, user_id: Text) -> Union[Text, SlackResponse]:
        # Достаём поле email из профиля пользователя

        try:
            user_info_response_data = self.client.users_info(user=user_id)
        except SlackApiError as api_error:
            raise ApiError(api_error).handle(self.client, self.data)

        if not user_info_response_data["user"]["is_bot"]:
            return user_info_response_data["user"]["profile"]["email"]
