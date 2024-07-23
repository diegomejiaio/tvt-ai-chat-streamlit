FROM python:3.10.14

WORKDIR /app

# Accept build arguments
ARG OPENAI_API_KEY

# Set environment variables
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY html_templates.py html_templates.py
COPY icons icons
COPY ui.py ui.py
COPY authentication.py authentication.py
COPY settings.yaml settings.yaml

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port", "8080", "--server.enableCORS", "false", "--server.address=0.0.0.0"]