import logging
import time
import psycopg2

DB_TIMEOUT = 180
CHECK_INTERVAL = 1

DB_CONFIG = {
    "host": "db", 
    "dbname": "ActivityLog", 
    "user": "postgres", 
    "password": "postgres"
}

start_time = time.time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def db_isready(config) -> None:
    """
    Check if the database is ready to accept connections, 
    If not, wait for it to be ready
    """
    while time.time() - start_time <  DB_TIMEOUT:
        try:
            conn = psycopg2.connect(**config)
            logger.info("Database is Ready!")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info("waiting for Database to be ready")
            time.sleep(CHECK_INTERVAL)
        
    logger.error(f"Cannot connect to DB within {DB_TIMEOUT} seconds")
    return False


db_isready(config=DB_CONFIG)
    