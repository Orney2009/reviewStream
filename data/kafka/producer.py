import time

import json

import requests

from kafka import KafkaProducer

from urllib.parse import quote_plus

MOVIES = ['adolescence', 'breaking bad', 'the crown', 'the 100', 'oppenheimer','wednesday', 'peaky blinders', 'stranger things', 'supernatural', 'euphoria']

KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]

USER_AGENT = "MovieSentimentBot/1.0"

producer = KafkaProducer(

    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

    value_serializer=lambda v: json.dumps(v).encode("utf-8"),

    key_serializer=lambda k: k.encode("utf-8") if k else None
)

dernier_posts = {movie: set() for movie in MOVIES}

def load_to_kafka():

    while True:

        for movie in MOVIES:

            subreddit = movie.replace(" ", "")

            url = f"https://www.reddit.com/r/{quote_plus(subreddit)}/new.json"

            headers = {"User-Agent": USER_AGENT}

            try:

                response = requests.get(url, headers=headers, timeout=10)

                if not response.ok:

                    print(f"[ERROR] Reddit API {subreddit} → {response.status_code}")

                    continue

                data = response.json()

                children = data.get("data", {}).get("children", [])

                posts = []

                ids_actuels = set()

                for child in children:

                    d = child.get("data", {})

                    post_id = d.get("id")

                    if not post_id:

                        continue

                    ids_actuels.add(post_id)

                    posts.append({

                        "id": post_id,

                        "subreddit": d.get("subreddit"),

                        "title": d.get("title"),

                        "selftext": d.get("selftext"),

                        "created_utc": d.get("created_utc"),

                        "author": d.get("author"),

                        "score": d.get("score"),

                        "num_comments": d.get("num_comments"),

                        "permalink": f"https://www.reddit.com{d.get('permalink', '')}",

                        "movie": movie
                    })

                nouveaux = ids_actuels - dernier_posts[movie]

                if nouveaux:

                    print(f"[INFO] {movie}: {len(nouveaux)} nouveaux posts détectés.")

                    for post in posts:

                        if post["id"] in nouveaux:

                            topic = movie.replace(" ", "_").lower()

                            producer.send(topic, key=post["id"], value=post)

                    producer.flush()

                else:

                    print(f"[INFO] {movie}: aucune nouveauté.")

                dernier_posts[movie] = ids_actuels

            except Exception as e:
                
                print(f"[FATAL] {movie}: {e}")

            time.sleep(0.2)

        time.sleep(5)


# if __name__ == "__main__":

#     main()
