# Установка и запуск бота.

---

## Установка и запуск через виртуальное окружение.

1. Установка виртуального окружения и зависимостей:

   ```bash  
   virtualenv /путь/до/репозитория/venv -p python3 # Python 3.6+ required
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Запуск:

    ```bash  
    ./venv/bin/python ./main.py
    ```

---

## Установка и запуск через docker:

```bash  
docker-compose up -d
```
