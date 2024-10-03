from flask import Flask, jsonify, render_template, request
from kafka import KafkaConsumer
import threading
import json
import queue
import re
from datetime import datetime
from pprint import pprint

app = Flask(__name__)

# Create a queue to store messages received by the Kafka consumer
message_queue = queue.Queue()
messages = []

# Function to parse and format syslog entries into JSON
def parse_syslog(log_entry):
    syslog_regex = r'(?P<timestamp>\S+) (?P<host>\S+) (?P<process>[\w-]+): (?P<message>.+)'
    match = re.match(syslog_regex, log_entry)
    
    if match:
        log_data = match.groupdict()
        # Format the timestamp into ISO 8601
        try:
            log_data['timestamp'] = datetime.strptime(log_data['timestamp'], "%Y-%m-%dT%H:%M:%S.%f-%z").isoformat()
        except ValueError:
            pass
        return log_data
    return None

# Function to run the Kafka consumer
def run_consumer(offset):
    consumer = KafkaConsumer(
    "syslog",
    bootstrap_servers=["localhost:19092"],
    group_id="demo-group",
    auto_offset_reset=offset,
    enable_auto_commit=True,
    consumer_timeout_ms=1000,
    )
    
    for msg in consumer:
        if msg is not None:
            msg = str(msg.value.decode('utf-8'))
            message_queue.put(msg)  # Decode to string


@app.route('/')
def index():
    run_consumer(offset="earliest")
    return render_template('index.html')

@app.route('/api/syslogs')
def get_syslogs():
    run_consumer(offset="latest")
    # Fetch up to 10 messages from the queue
    while not message_queue.empty():
        msg = parse_syslog(message_queue.get())
        print(msg)
        if msg is not None:
            messages.append(msg)

    # Return the messages as a JSON response
    return jsonify(messages)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
