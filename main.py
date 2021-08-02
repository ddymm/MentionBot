from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


APP_TOKEN = "xapp-*"
BOT_TOKEN = "xoxb-*"


app = App(token=BOT_TOKEN)


@app.event("app_mention")
def mention_event(client, body):
    event = body["event"]

    # Хак, чтобы меншны работали и из каналов, и из тредов.
    ts = event.get("thread_ts", event["event_ts"])

    # Достаём списки заменшненых групп и пользователей из сообщения.
    mentioned_groups = [
        obj["usergroup_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "usergroup"
    ]
    mentioned_users = [obj["user_id"] for obj in event["blocks"][0]["elements"][0]["elements"] if obj["type"] == "user"]

    if not mentioned_groups and len(mentioned_users) == 1:  # len(mentioned_users) == 1 -> когда заменшнен только бот
        return client.chat_postMessage(text="Некорректный запрос.", thread_ts=ts, channel=event["channel"])

    client.chat_postMessage(text="Собираю данные...", thread_ts=ts, channel=event["channel"])

    # Получаем списки пользователей каждой группы по id.
    users_list_response_data = [client.usergroups_users_list(usergroup=group_id) for group_id in mentioned_groups]

    # Достаём id пользователей из списков групп и добавляем в список заменшных пользователей.
    for group in users_list_response_data:
        for user_id in group["users"]:
            mentioned_users.append(user_id)

    # Получаем профили пользователей по id (приводим список к set -> не генерим лишние запросы к API).
    user_info_response_data = [client.users_info(user=user_id) for user_id in set(mentioned_users)]

    # Достаём из профилей поле email (у пользователей-ботов этого поля нет, поэтому используем метод .get("key")).
    email_list = [user["user"]["profile"].get("email") for user in user_info_response_data]

    # Готовим текст ответа от бота (фильтруем от None в случае с ботом, сортируем для красоты).
    response_text = "\n".join(sorted(filter(None, email_list))) or "Не получилось найти :("

    return client.chat_postMessage(text=response_text, thread_ts=ts, channel=event["channel"])


if __name__ == "__main__":
    SocketModeHandler(app, APP_TOKEN).start()
