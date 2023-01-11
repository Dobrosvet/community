import os

from airtable import Airtable
from dotenv import load_dotenv

# Загрузить переменные окружения из файла `.env`
load_dotenv()

api_key = os.environ['AIRTABLE_API_KEY']
base_id = os.environ['AIRTABLE_BASE_ID']

user_table_name = os.environ['AIRTABLE_USER_TABLE_NAME']
card_table_name = os.environ['AIRTABLE_CARD_TABLE_NAME']

user_airtable = Airtable(base_id, user_table_name, api_key)
card_airtable = Airtable(base_id, card_table_name, api_key)
