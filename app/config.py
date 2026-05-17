from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC = os.getenv('ANTHROPIC_API_KEY')

EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY')
EVOLUTION_INSTANCE = os.getenv('EVOLUTION_INSTANCE', 'anamnese-bot')

APP_ENV = os.getenv('APP_ENV')