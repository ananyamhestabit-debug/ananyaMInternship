import logging
import os

LOG_DIR = "src/logs"
LOG_FILE = os.path.join(LOG_DIR, "image_rag.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    print("[INFO]", message)
    logging.info(message)

def log_error(message):
    print("[ERROR]", message)
    logging.error(message)