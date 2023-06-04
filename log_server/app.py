import fcntl
import json
import os
import logging
import time
import threading

from flask import Flask, request

from constants import (
    LOG_BUFFER_SIZE,
    LOG_FILE_PATH,
    LOG_FLUSH_INTERVAL
)
from database import *

# Add logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


app = Flask(__name__)
db_driver = DatabaseDriver()
db_driver.connect_db()

# Need to run this before first request
@app.before_first_request
def setup():
    flush_logs_thread = threading.Thread(target=flush_logs_periodically)
    flush_logs_thread.start()


@app.route('/log', methods=['POST'])
def log_handler():
    log_data = request.json
    append_log_to_file(log_data)

    if os.path.getsize(LOG_FILE_PATH) > LOG_BUFFER_SIZE:
        db_driver.flush_logs_to_db()
    return "Accepted\n"


def append_log_to_file(log_data):
    with open(LOG_FILE_PATH, "a") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        json.dump(log_data, file)
        file.write("\n")
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)


def flush_logs_periodically():
    while True:
        time.sleep(LOG_FLUSH_INTERVAL)
        logger.info(f"Auto flush logs called at {time.time()}")
        db_driver.flush_logs_to_db()
