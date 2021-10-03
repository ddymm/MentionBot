FROM python:3.8
RUN useradd -m bot_user
USER bot_user
WORKDIR /home/bot_user/code
ENV PATH="/home/bot_user/.local/bin:${PATH}"
COPY --chown=bot_user:bot_user . .

RUN pip install --user -r requirements.txt
