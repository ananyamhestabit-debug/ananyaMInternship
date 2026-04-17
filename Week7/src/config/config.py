# loads environment vars/sys. configs(keys,paths)
import os
from dotenv import load_dotenv 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  #takes api key
DB_PATH = "database/sample.db"  #db location defines