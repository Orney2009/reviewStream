from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import json


load_dotenv()

topic_name = os.getenv('TOPIC_LOADER_NAME')

def consumer_loader(topic_name):

    consumer_loader = KafkaConsumer(
        topic_name,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True
    )

    return consumer_loader 



























