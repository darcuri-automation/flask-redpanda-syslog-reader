from flask import Flask, jsonify
from kafka import KafkaConsumer
import threading
import json
import queue

app = Flask(__name__)

# Create a queue to store messages received by the Kafka consumer
message_queue = queue.Queue()

# Function to run the Kafka consumer
def run_consumer():
    consumer = KafkaConsumer(
    "syslog",
    bootstrap_servers=["localhost:19092"],
    group_id="demo-group",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=1000,
    )
    
    for msg in consumer:
        print(f"MESSAGE: {msg.value}")
        message_queue.put(str(msg.value))  # Decode to string


@app.route('/')
def index():
    return f"<p>Flask app is running and listening for <a href=\"http://127.0.0.1:5000/messages\">syslog messages.</a><br>"

@app.route('/messages')
def get_messages():
    messages = []
    run_consumer()

    # Fetch up to 10 messages from the queue
    while not message_queue.empty():
        messages.append(message_queue.get())
    
    # Return the messages as a JSON response
    return jsonify(messages)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
