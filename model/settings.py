import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
USER_TEST=os.getenv('USER_TEST')
PASSWORD=os.getenv('PASSWORD')
CHANNEL_ACCESS_TOKEN=os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET=os.getenv('CHANNEL_SECRET')
NGROK_URL=os.getenv('NGROK_URL')