## Первичная настройка:

---

* Создать [Slack App](https://api.slack.com/apps).
* Установить бота в workspace.
* Создать файл `.env` в корне проекта, скопировать содержимое из `.env.template`:

    ```bash
    cp .env.template .env
    ```
  
* В файле `.env` переопределить значения `APP_TOKEN` токеном из раздела `App-Level Tokens`.
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
