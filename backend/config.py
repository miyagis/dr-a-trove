import json
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


def logging_setup():
    log_dir = "backend\\logging"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define the log file path with the current date
    log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

    # Configure the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a handler that writes log messages to a file and rotates the log file daily
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7, encoding='utf-8')
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
    return logger

def set_env_variables():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = get_langchain_api_key()
    os.environ["OPENAI_API_KEY"] = get_chatGPT_api_key()
    os.environ["GOOGLE_CSE_ID"] = get_google_cse_id()
    os.environ["GOOGLE_API_KEY"] = get_gemini_api_key()
    os.environ["TAVILY_API_KEY"] = get_tavily_api_key()

def get_gemini_api_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["gemini_api_key"]
        secrets_file.close()
        return my_secret

def get_tavily_api_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["tavily_api_key"]
        secrets_file.close()
        return my_secret

def get_google_api_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["google_api_key"]
        secrets_file.close()
        return my_secret
    
def get_google_cse_id():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["google_cse_id"]
        secrets_file.close()
        return my_secret
    
def get_search_brave_token():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["search_brave_token"]
        secrets_file.close()
        return my_secret

def get_langchain_api_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["langchain_api_key"]
        secrets_file.close()
        return my_secret

def get_azure_language_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["azure_language_key"]
        secrets_file.close()
        return my_secret


def get_azure_language_endpoint():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["azure_language_endpoint"]
        secrets_file.close()
        return my_secret


def get_googleCloud_API_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["googleCloud_API_key"]
        secrets_file.close()
        return my_secret

def get_googleCloud_API_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["googleCloud_API_key"]
        secrets_file.close()
        return my_secret


def get_twitter_api_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["twitter_api_key"]
        secrets_file.close()
        return my_secret


def get_twitter_api_key_secret():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["twitter_api_key_secret"]
        secrets_file.close()
        return my_secret


def get_twitter_bearer_token():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["twitter_bearer_token"]
        secrets_file.close()
        return my_secret


def get_chatGPT_api_key():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["chatGPT_api_key"]
        secrets_file.close()
        return my_secret


def get_chatGPT_org_name():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["chatGPT_org_name"]
        secrets_file.close()
        return my_secret


def get_chatGPT_org_ID():
    with open("backend\\secrets.json") as secrets_file:
        my_content = json.load(secrets_file)
        my_secret = my_content["chatGPT_org_ID"]
        secrets_file.close()
        return my_secret
