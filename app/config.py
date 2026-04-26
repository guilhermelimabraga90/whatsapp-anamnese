from dotenv import load_dotenv
import os

load_dotenv()

WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ANTHROPIC = os.getenv('ANTHROPIC_API_KEY')

APP_ENV = os.getenv('APP_ENV')