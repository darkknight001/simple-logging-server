import json
import os

import psycopg2
import psycopg2.extras

from constants import (
    DB_HOSTNAME,
    DB_PASSWORD,
    DB_USER,
    LOGS_DB,
    LOG_FILE_PATH
)

class DatabaseDriver:
    """
    Database driver to connect to the database and flush logs to the database 
    """
    def __init__(self) -> None:
        self.conn = None

    def connect_db(self) -> None:
        conn = psycopg2.connect(
                host=DB_HOSTNAME, 
                dbname=LOGS_DB, 
                user=DB_USER, 
                password=DB_PASSWORD
            )
        self.conn = conn

    def flush_logs_to_db(self):
        if os.path.isfile(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as file:
                logs = file.readlines()
                try:
                    cursor = self.conn.cursor()
                    records = []
                    for log in logs:
                        log_data = json.loads(log)
                        record = (
                            log_data['id'],
                            log_data['unix_ts'],
                            log_data['user_id'],
                            log_data['event_name']
                        )
                        records.append(record)

                    sql = "INSERT INTO logs (id, unix_ts, user_id, event_name) VALUES (%s, %s, %s, %s)"
                    psycopg2.extras.execute_batch(cursor, sql, records)
                    self.conn.commit()

                except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
                    self.conn.rollback()
                    return
                
                os.remove(LOG_FILE_PATH)


