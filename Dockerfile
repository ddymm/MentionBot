FROM python:3.8
WORKDIR /bot/
COPY . .
RUN pip install --user -r requirements.txt
