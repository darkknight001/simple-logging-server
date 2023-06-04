import argparse
import json
import requests
import time
import threading
import random

url = "http://webserver:5000/log"

EVENT_CHOICES = ["logout", "login", "some_event"]

def send_request():
    data = {
        "id": random.randint(1000,100000),
        "unix_ts": int(time.time()),
        "user_id": random.randint(1000,100000),
        "event_name": random.choice(EVENT_CHOICES)
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Request sent successfully")
    else:
        print("Failed to send request")

def send_requests_thread(duration=None):
    start_time = time.time()
    end_time = start_time + duration if duration else None

    while end_time is None or time.time() < end_time:
        send_request()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, help='Duration in seconds')
    args = parser.parse_args()

    # Get the duration from command line arguments
    duration = args.duration

    # Start the threads
    num_threads = 10
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=send_requests_thread, args=(duration,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish if duration is provided
    if duration:
        for thread in threads:
            thread.join()
    else:
        # Allow the script to run indefinitely until user interrupts
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
