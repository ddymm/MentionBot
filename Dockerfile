FROM python:3.8

# PIPу не нравится установка зависимостей глобально - просто создадим пользователя для запуска внутри контейнера
RUN useradd -m bot_user
USER bot_user
ENV PATH="/home/bot_user/.local/bin:${PATH}"

# Копируем проект внутрь контейнера под созданным пользователем
WORKDIR /home/bot_user/code
COPY --chown=bot_user:bot_user . .

# Установка зависимостей под созданным пользователем
RUN pip install --user -r requirements.txt
