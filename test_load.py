# from data import db
from lib import Model
import os
from consumer import consumer_realtime_to_file
from consumer import consumer_loader_data
import threading
from dotenv import load_dotenv



load_dotenv()

topic_name = os.getenv('TOPIC_LOADER_NAME')


# db.create_tables()

test = Model()
results = test.predict(["Avoid this movie at all costs, everything about it is bad", "I love it", "It's a great movie !"])

print(results)
# for result in results:
#     print(result)

# print(consumer_loader_data(topic_name))


consumer_loader_data(topic_name)



print("Done!")


