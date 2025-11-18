"""
this file create a connection instance to the postgresql database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from lib import imdb_file_path, pg_database, pg_dialect_and_driver, pg_host, pg_password, pg_port, pg_username
from .base import Base
from ..models import Shows, Reviews

url_object = URL.create(
    pg_dialect_and_driver,
    username=pg_username,
    password=pg_password,
    host=pg_host,
    port=pg_port,
    database=pg_database,
)

engine = create_engine(url_object, echo=True)


# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class db:
    """
    connection instance. enable creation of the databases (more to come)
    """

    # creation des tables
    def create_tables() -> None:
        """
        drop and recreate all the tables (for instance, Reviews and Shows)
        """

        print("\n\nDrop existing tables...\n\n")
        Base.metadata.reflect(bind=engine, resolve_fks=False)
        Base.metadata.drop_all(bind=engine)
        print("\n\nTables dropped successfully !\n\n")
        print("\n\nCreation of the tables...\n\n")
        Base.metadata.create_all(bind=engine)
        print("\n\nTables created successfully !\n\n")