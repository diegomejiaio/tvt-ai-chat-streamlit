# Procafecol Assistant

## Overview

Welcome to the TVT AI Chat Streamlit project! This project aims to provide a basic chatbot using OpenAI API keys. 

## Deploy localy

To get started, follow these simple steps:

1. **Create a Virtual Environment**: Start by creating a virtual environment for the project. You can use Python 3.10.12 and run the following command: `python3 -m venv chat_venv`

2. **Activate the Virtual Environment**: Activate the virtual environment by running the following command: `source chat_venv/bin/activate`

3. **Upgrade pip**: Make sure you have the latest version of pip installed by running: `pip install --upgrade pip`

4. **Install Requirements**: Install the required packages by running: `pip install -r requirements.txt`

   **Note for Windows Users**: If you encounter any installation errors, please open an issue on GitHub.

5. **Run the Application**: Start the application by running the following command in your terminal: `streamlit run main.py`

Now you're ready to use the TVT AI Chat Streamlit project! Enjoy chatting with the chatbot.



## Configure a new assistant

1. Go to settings and modify parameters in `settings.yaml`
   
   1. **UI**
      - password
      - pagetitle
      - sidebar
        - title
        - option1
        - option2
        - option3
      - greeting
      - placeholder
      - bot_name
      - person_name
      - instructions 

2. Go to `./chat_icons` and change images keeping the names.