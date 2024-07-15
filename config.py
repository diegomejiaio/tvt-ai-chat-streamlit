import yaml
import os
from dotenv import load_dotenv

def load_settings(file_path):
    with open(file_path, "r") as file:
        settings = yaml.safe_load(file)
    return settings

def load_api_key():
    load_dotenv()
    return os.getenv("OPEN_API_KEY")
