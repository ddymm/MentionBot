# Деплой бота на удалённый сервер (сборка и запуск через docker)

---

### Первичная настройка:

1. Установить **ansible**:

    ```bash
    pip install -r requirements_dev.txt
    ```

2. Создать файл `hosts.yml` в директории `./playbooks`, 
скопировать содержимое из `hosts.yml.template`,
переопределить параметрами своего хоста для деплоя.

---

### Использование:

Все команды выполняются **из-под директории playbooks**.

* Деплой со сборкой и запуском бота:

    ```bash
    ansible-playbook -i playbooks/hosts.yml playbooks/deploy.yml
    ```
  
* Перезапуск бота (остановка контейнера, сборка и запуск):

    ```bash
    ansible-playbook -i playbooks/hosts.yml playbooks/deploy.yml --tags=restart
    ```
