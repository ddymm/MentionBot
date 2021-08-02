# MentionBot для Slack.
## Описание:
Бот для Slack, который в ответ на меншны user-групп и / или пользователей возвращает список email пользователей, который можно вставить в поле для отправки приглашений в ивенте gcal.

## Первичная настройка:
* Создать [Slack App](https://api.slack.com/apps).
* Установить бота в workspace.
* Переименовать файл `.env.template` -> `.env`
* В файле переопределить значения `APP_TOKEN` в `.env` токеном из раздела `App-Level Tokens`.
* На странице `Features -> OAuth & Permissions`:
  * В разделе `Scopes -> Bot Token Scopes` добавить следующие права боту:
    * `app_mentions:read`
    * `chat:write`
    * `usergroups:read`
    * `users:read`
    * `users:read.email`
  * Переопределить значения `BOT_TOKEN` в `.env` токеном из поля `Bot User OAuth Token` с этой страницы.
* На странице `Features -> Event Subscriptions`:
  * Активировать чекбокс `Enable Events`.
  * В разделе `Subscribe to bot events` добавить ивент `app_mention`.

## Особенности:
* Бот умеет работать как с упоминанием user-group, так и с упоминанием пользователей.
* Чем больше пользователей в упомянутых группах / упомянуто => тем дольше придётся ждать ответа от бота.
