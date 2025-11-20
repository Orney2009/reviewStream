import json

import time

import requests

from kafka import KafkaProducer

from urllib.parse import quote_plus

from collections import deque

REDDIT_USER_AGENT = "MovieSentimentBot/1.0"

KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]

# On ajuste la limite pour récupérer assez de posts pour faire du streaming

LIMIT_POSTS = 50

# On définit la variable contennat le nom des films : MOVIES

MOVIES = ['adolescence',
                    'breaking bad',
                    'the crown',
                    'the 100',
                    'oppenheimer',
                    'wednesday',
                    'peaky blinders',
                    'stranger things',
                    'supernatural',
                    'euphoria'
]

# Dictionnaire global pour stocker les files d'attente des posts pour chaque film

POST_QUEUES = {}


def build_subreddit_name(movie_name: str) -> str:
    """Construit le nom du subreddit en enlevant les espaces."""
    return movie_name.replace(" ", "")


def build_topic_name(movie_name: str) -> str:
    """Construit le nom du topic Kafka en minuscules avec underscores."""
    return movie_name.replace(" ", "_").lower()


def build_reddit_url(subreddit: str) -> str:
    """Construit l'URL de l'API Reddit pour un subreddit."""
    return f"https://www.reddit.com/r/{quote_plus(subreddit)}/new.json"


def build_request_headers() -> dict:
    """Construit les headers HTTP pour l'API Reddit."""
    return {"User-Agent": REDDIT_USER_AGENT}


def build_request_params(limit: int) -> dict:
    """Construit les paramètres de la requête."""
    return {"limit": str(limit)}


def make_reddit_request(url: str, headers: dict, params: dict) -> requests.Response:
    """Fait la requête HTTP vers Reddit."""
    return requests.get(url, headers=headers, params=params, timeout=10)


def extract_post_data(child_data: dict) -> dict:
    """Extrait les données importantes d'un post Reddit."""
    return {
        "id": child_data.get("id"),
        "subreddit": child_data.get("subreddit"),
        "title": child_data.get("title"),
        "selftext": child_data.get("selftext"),
        "created_utc": child_data.get("created_utc"),
        "author": child_data.get("author"),
        "score": child_data.get("score"),
        "num_comments": child_data.get("num_comments"),
        "permalink": f"https://www.reddit.com{child_data.get('permalink', '')}",
    }


def parse_reddit_response(response_data: dict) -> list:
    """Parse la réponse JSON de Reddit et retourne une liste de posts."""
    children = response_data.get("data", {}).get("children", [])
    posts = []
    for child in children:
        child_data = child.get("data", {})
        post = extract_post_data(child_data)
        posts.append(post)
    return posts


def fetch_reddit_posts(subreddit: str, limit: int = LIMIT_POSTS) -> list:
    """Récupère les posts d'un subreddit."""
    url = build_reddit_url(subreddit)
    headers = build_request_headers()
    params = build_request_params(limit)
    response = make_reddit_request(url, headers, params)

    if not response.ok:
        print(f"[ERROR] Reddit API {subreddit} status={response.status_code}")
        return []

    response_data = response.json()
    return parse_reddit_response(response_data)


# ============= FONCTIONS KAFKA =============

def create_value_serializer():
    """Crée la fonction de sérialisation pour les valeurs."""
    return lambda v: json.dumps(v).encode("utf-8")


def create_key_serializer():
    """Crée la fonction de sérialisation pour les clés."""
    return lambda k: k.encode("utf-8") if k else None


def create_kafka_producer() -> KafkaProducer:
    """Crée et configure un producer Kafka."""
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=create_value_serializer(),
        key_serializer=create_key_serializer(),
    )


def add_movie_metadata(post: dict, movie_name: str) -> dict:
    """Ajoute le nom du film au post."""
    post["movie"] = movie_name
    return post


def send_post_to_kafka(producer: KafkaProducer, topic_name: str, post: dict) -> bool:
    """Envoie un post dans Kafka. Retourne True si succès."""
    try:
        producer.send(
            topic_name,
            key=post.get("id", ""),
            value=post,
        )
        print(f"[SUCCESS] Envoi topic={topic_name} id={post.get('id')[:5]}...")
        return True
    except Exception as e:
        print(f"[ERROR] Envoi Kafka pour topic={topic_name} id={post.get('id')}: {e}")
        return False


def wait_between_requests(seconds: int = 5):
    """Attend entre les requêtes."""
    time.sleep(seconds)


# ============= NOUVELLES FONCTIONS DE TRAITEMENT EN STREAMING =============

def initialize_queues():
    """Initialise les files d'attente pour tous les films."""
    print("Initialisation des files d'attente...")
    for movie in MOVIES:
        subreddit_name = build_subreddit_name(movie)
        posts = fetch_reddit_posts(subreddit_name, LIMIT_POSTS)
        POST_QUEUES[movie] = deque(posts)
        print(f"  > '{movie}': {len(posts)} posts prêts.")


def send_next_stream_element(producer: KafkaProducer, movie_name: str):
    """Envoie le prochain élément d'un film vers Kafka."""
    queue = POST_QUEUES.get(movie_name)
    topic_name = build_topic_name(movie_name)

    if not queue:
        print(f"[WARN] File d'attente vide ou inexistante pour {movie_name}")
        return

    # Si la queue est presque vide, on recharge les données pour le streaming continu
    if len(queue) < 5:
        subreddit_name = build_subreddit_name(movie_name)
        new_posts = fetch_reddit_posts(subreddit_name, LIMIT_POSTS)
        queue.extend(new_posts)
        print(f"[INFO] Rechargement de données pour {movie_name}. Nouvelle taille: {len(queue)}")

    if queue:
        post = queue.popleft()  # Prend le premier élément de la file
        post = add_movie_metadata(post, movie_name)
        send_post_to_kafka(producer, topic_name, post)
        producer.flush()


def stream_data_continuously(producer: KafkaProducer, movies: list):
    """Boucle principale de streaming."""
    initialize_queues()
    print("\n--- Démarrage du streaming continu (1 post toutes les 5s) ---")

    # Utilisation de cycle pour alterner entre les films indéfiniment
    from itertools import cycle
    movie_cycle = cycle(movies)

    while True:
        try:
            current_movie = next(movie_cycle)
            send_next_stream_element(producer, current_movie)
            wait_between_requests(seconds=5)  # Attente de 5 secondes
        except KeyboardInterrupt:
            print("\nArrêt du streaming par l'utilisateur.")
            break
        except Exception as e:
            print(f"[FATAL ERROR] {e}")
            break


# ============= FONCTION PRINCIPALE =============

def main():
    """Point d'entrée principal du programme."""
    producer = create_kafka_producer()

    stream_data_continuously(producer, MOVIES)  # Appel de la nouvelle fonction de streaming

    producer.close()
    print("Terminé.")


if __name__ == "__main__":
    main()
