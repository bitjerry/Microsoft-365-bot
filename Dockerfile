FROM python:3.10.8

ENV BOT_TOKEN ""
ENV ADMIN_ID ""
#ENV DATABASE_URL ""
#WEBHOOK_URL ""
#BOT_LANG ""

WORKDIR /bot

COPY /src requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "setup.py"]

