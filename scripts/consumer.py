from kafka import KafkaConsumer


def syslog_subscriber():
    data = {}

    consumer = KafkaConsumer(
    bootstrap_servers=["localhost:19092"],
    group_id="demo-group",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=1000
    )

    consumer.subscribe("syslog")

    try:
        for message in consumer:
            topic_info = f"topic: {message.partition}|{message.offset})"
            message_info = f"key: {message.key}, {message.value}"
            print(f"{topic_info}, {message_info}")

            data[topic_info] = message_info
    except Exception as e:
        return f"Error occurred while consuming messages: {e}"
    finally:
        consumer.close()
        return data