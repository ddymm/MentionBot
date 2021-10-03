# Деплой бота на удалённый сервер (сборка и запуск через docker)

---

### Первичная настройка:

1. Установить **ansible**:

    ```bash
    pip install ansible
    ```

2. Создать файл `hosts.yml` в директории `./playbooks`, 
скопировать содержимое из `hosts.yml.template`,
переопределить параметрами своего хоста для деплоя.

---

### Использование:

Все команды выполняются **из-под директории playbooks**.

* Деплой со сборкой и запуском бота:

    ```bash
    ansible-playbook -i hosts.yml deploy.yml --tags=deploy
    ```
  
* Перезапуск бота (остановка контейнера, сборка и запуск):

    ```bash
    ansible-playbook -i hosts.yml deploy.yml --tags=restart
    ```
