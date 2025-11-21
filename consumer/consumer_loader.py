from kafka import KafkaConsumer
import os
import json


def consumer_loader_data(topic_name):

    consumer_loader = KafkaConsumer(
        topic_name,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True
    )

    for element in consumer_loader:
        print(element.value)



    return consumer_loader 



























