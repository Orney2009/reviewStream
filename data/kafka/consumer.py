from kafka import KafkaConsumer

import json

# CONFIGURATION 
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
CONSUMER_TIMEOUT_MS = 5000
MAX_MESSAGES_TO_DISPLAY = 5

def create_value_deserializer():
    return lambda x: json.loads(x.decode('utf-8'))

def create_kafka_consumer(topic_name: str) -> KafkaConsumer:
    """Crée et configure un consumer Kafka pour un topic."""
    return KafkaConsumer(
        topic_name,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        value_deserializer=create_value_deserializer(),
        consumer_timeout_ms=CONSUMER_TIMEOUT_MS
    )


def close_consumer(consumer: KafkaConsumer):
    consumer.close()

def extract_title(message_value: dict) -> str:
    return message_value.get('title', 'N/A')


def extract_selftext(message_value: dict) -> str:
    return message_value.get('selftext', '')


def extract_author(message_value: dict) -> str:
    return message_value.get('author', 'N/A')


def extract_score(message_value: dict) -> int:
    return message_value.get('score', 0)


def extract_subreddit(message_value: dict) -> str:
    return message_value.get('subreddit', 'N/A')


def extract_num_comments(message_value: dict) -> int:
    return message_value.get('num_comments', 0)


def print_topic_header(topic_name: str):
    print(f"\n=== Messages du topic '{topic_name}' ===")

def print_post_separator(post_number: int):
    print(f"\n--- Post {post_number} ---")

def print_post_title(title: str):
    print(f"Titre: {title}")


def print_post_selftext(selftext: str):
    print(f"Contenu: {selftext}")


def print_post_author(author: str):
    print(f"Auteur: {author}")


def print_post_score(score: int):
    print(f"Score: {score}")


def print_post_subreddit(subreddit: str):
    print(f"Subreddit: {subreddit}")


def print_post_comments(num_comments: int):
    print(f"Commentaires: {num_comments}")


def print_total_messages(count: int):
    print(f"\nTotal: {count} messages affichés")

def display_post_details(message_value: dict, post_number: int):
    print_post_separator(post_number)
    print_post_title(extract_title(message_value))
    print_post_selftext(extract_selftext(message_value))
    print_post_author(extract_author(message_value))
    print_post_score(extract_score(message_value))
    print_post_subreddit(extract_subreddit(message_value))
    print_post_comments(extract_num_comments(message_value))


def should_stop_consuming(count: int, max_messages: int) -> bool:
    return count >= max_messages


def consume_messages(consumer: KafkaConsumer, max_messages: int = MAX_MESSAGES_TO_DISPLAY) -> int:
    count = 0

    for message in consumer:
        display_post_details(message.value, count + 1)
        count += 1

        if should_stop_consuming(count, max_messages):
            break

    return count


def process_topic(topic_name: str, max_messages: int = MAX_MESSAGES_TO_DISPLAY):
    print_topic_header(topic_name)

    consumer = create_kafka_consumer(topic_name)
    count = consume_messages(consumer, max_messages)
    close_consumer(consumer)

    print_total_messages(count)


def test_multiple_topics(topic_names: list):
    for topic_name in topic_names:
        process_topic(topic_name)


def main():
    topics_to_test = ['queensgambit', 'breakingbad']
    test_multiple_topics(topics_to_test)


if __name__ == "__main__":
    main()