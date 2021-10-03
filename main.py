# -*- coding: utf-8 -*-
from typing import Dict, List, Text
from dotenv import dotenv_values
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import SlackResponse
from slack_sdk.web.client import WebClient
from bot import MentionBot


CONFIG = dotenv_values(".env")
APP = App(token=CONFIG["BOT_TOKEN"])


@APP.event("app_mention")
def handle(client: WebClient, body: Dict) -> SlackResponse:
    bot = MentionBot(client, body)

    # Достаём список id заменшненых групп и список id пользователей из ивента-упоминания бота.
    user_ids, group_ids = bot.get_data_from_message(body["event"])

    # Достаём список id пользователей из каждой группы, добавляем к списку пользователей.
    for group_id in group_ids:
        user_ids += bot.get_users_list_from_group(group_id)

    # Достаём поле email из профиля каждого пользователя. Приводим к set -> не генерим лишние запросы к API.
    email_list: List[Text] = [bot.get_email_from_user(user_id) for user_id in set(user_ids)]

    # Готовим текст ответа.
    text: Text = "\n".join(sorted(filter(None, email_list))) or "Не получилось найти :("

    return bot.send_message(text=text)


if __name__ == "__main__":
    SocketModeHandler(APP, CONFIG["APP_TOKEN"]).start()
