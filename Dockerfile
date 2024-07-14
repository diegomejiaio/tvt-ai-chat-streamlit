FROM python:3.10.14

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY html_templates.py html_templates.py
COPY .env .env
COPY chat_icons chat_icons

RUN pip install -r requirements.txt

EXPOSE 8501

CMD streamlit run main.py
