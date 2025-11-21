"""
this file define all the variables commonly used accross the project (like the env variables)
"""

from dotenv import load_dotenv
import os

load_dotenv()

# csv file path
imdb_file_path = os.getenv("IMDB_FILE_PATH")

# postgres connections information
pg_dialect_and_driver = os.getenv("PG_DIALECT_AND_DRIVER")
pg_username = os.getenv("PG_USERNAME")
pg_password = os.getenv("PG_PASSWORD")
pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_database = os.getenv("PG_DATABASE")

# pickles file path
model_file_path = os.getenv("MODEL_PICKLE_FILE_PATH")
vector_file_path = os.getenv("VECTOR_PICKLE_FILE_PATH")

# stopwords file path
stopwords_file_path = os.getenv("STOPWORDS_FILE_PATH")