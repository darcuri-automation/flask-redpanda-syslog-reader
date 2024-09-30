import json
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(
    bootstrap_servers = "localhost:19092",
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

topic = "syslog"

def on_success(metadata):
  print(f"Message produced to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

# Produce asynchronously with callbacks
for i in range(10, 21):
  msg = { "id": i, "content": "Some value"}
  future = producer.send(topic, msg)
  future.add_callback(on_success)
  future.add_errback(on_error)

producer.flush()
producer.close()