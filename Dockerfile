FROM rasa/rasa-sdk:latest

WORKDIR /app

COPY run-requirements.txt /app/requirements.txt

COPY output-kb /app/output-kb

USER root

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY actions /app/actions

USER 1001

EXPOSE 5055
