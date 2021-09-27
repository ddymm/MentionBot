# -*- coding: utf-8 -*-

from dotenv import dotenv_values
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import SlackResponse
from slack_sdk.web.client import WebClient
from typing import Dict, List, Text


config = dotenv_values(".env")


app = App(token=config["BOT_TOKEN"])


def _send_message(client: WebClient, data: Dict, text: Text) -> SlackResponse:
    return client.chat_postMessage(text=text, **data)


def _get_data_from_message(event: Dict) -> Dict:
    # Достаём списки заменшненых групп и пользователей из ивента-упоминания бота.

    mentioned_users: List = [
        obj["user_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "user"
    ]

    mentioned_groups: List = [
        obj["usergroup_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "usergroup"
    ]

    return {"user_ids": list(set(mentioned_users)), "group_ids": list(set(mentioned_groups))}


def _get_users_list_from_group(client: WebClient, group_id: Text) -> List[Text]:
    # Достаём список пользователей из группы.

    users_list_response_data = client.usergroups_users_list(usergroup=group_id)

    return users_list_response_data["users"]


def _get_email_from_user(client: WebClient, user_id: Text) -> Text:
    # Достаём поле email из профиля пользователя

    # Получаем профиль пользователя по id.
    user_info_response_data = client.users_info(user=user_id)

    if not user_info_response_data["user"]["is_bot"]:
        return user_info_response_data["user"]["profile"]["email"]


@app.event("app_mention")
def mention_event(client: WebClient, body: Dict) -> SlackResponse:
    event: Dict = body["event"]

    response_data: Dict = {
        "thread_ts": event.get("thread_ts", event["event_ts"]),  # Хак, чтобы меншны работали и из каналов, и из тредов.
        "channel": event["channel"],
    }

    data: Dict = _get_data_from_message(event)

    if not data["group_ids"] and len(data["user_ids"]) == 1:  # когда заменшнен только бот.
        return _send_message(client, response_data, text="Некорректный запрос.")

    else:
        _send_message(client, response_data, text="Собираю данные...")

    for group_id in data["group_ids"]:
        data["user_ids"] += _get_users_list_from_group(client, group_id)

    email_list: List[Text] = [_get_email_from_user(client, user_id) for user_id in set(data["user_ids"])]

    # Готовим текст ответа от бота (фильтруем от None в случае с ботом, сортируем для красоты).
    text: Text = "\n".join(sorted(filter(None, email_list))) or "Не получилось найти :("

    return _send_message(client, response_data, text=text)


if __name__ == "__main__":
    SocketModeHandler(app, config["APP_TOKEN"]).start()
