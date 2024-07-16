FROM python:3.10.14

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY html_templates.py html_templates.py
COPY .env .env
COPY icons icons
COPY ui.py ui.py
COPY autentication.py autentication.py

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "streamlit","run","main.py","--server.port","8080", "--server.enableCORS", "false", "--server.address=0.0.0.0" ]