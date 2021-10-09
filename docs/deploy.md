# Деплой бота на удалённый сервер (сборка и запуск через docker)

---

### Первичная настройка:

1. Установить **ansible**:

    ```bash
    pip install -r requirements_deploy.txt
    ```

2. Создать файл `hosts.yml` в директории `./playbooks`, 
скопировать содержимое из `hosts.yml.template`:

    ```bash
    cp playbooks/hosts.yml.template playbooks/hosts.yml
    ```

4. Переопределить переменные своего хоста для деплоя.

---

### Использование:

* Деплой со сборкой и запуском бота:

    ```bash
    ansible-playbook -i playbooks/hosts.yml playbooks/deploy.yml
    ```
  
* Простые действия можно выполнять с помощью запуска плейбука с указанием тега.
Список доступных тегов:

    * `stop` -> Остановка контейнера.
    * `start` -> Сборка контейнера и запуск.
    * `restart` -> Состоит из двух предыдущих шагов.

    Пример использования:

    ```bash
    ansible-playbook -i playbooks/hosts.yml playbooks/deploy.yml --tags=restart
    ```
