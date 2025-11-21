
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id='my_admin_client'
)

broker_address="localhost:9092"

topic_list = [
    NewTopic(
        name="peaky_blinders",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="wednesday",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="stranger_things",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="death_of_unicorn",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="la_casa_del_papel",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="le_parrain",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="adolescence",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="you",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="supernatural",
        num_partitions=1,
        replication_factor=1
    ),
    NewTopic(
        name="grey_anatomy",
        num_partitions=1,
        replication_factor=1
    )
]

def create_topic(topic_list):
    try:
        futures = admin_client.create_topics(new_topics=topic_list)
        print(futures)
        for topic, future in futures:
            future.result() # Peut lancer une exception si l'opération échoue
            print("Topic Created Successfully")
    except TopicAlreadyExistsError:
        print("Topic Already Exist.")
    except Exception as e:
        print(f"An error has occurred : {e}")


create_topic(topic_list)

    
    
    
    
   