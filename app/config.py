import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env


class Config:
    API_KEY = os.getenv('API_KEY')
    COHERE_KEY = os.getenv('COHERE_KEY')