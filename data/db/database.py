"""
this file create a connection instance to the postgresql database
"""

from sqlalchemy import create_engine, select
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
session = SessionLocal()

class db:
    """
    connection instance. enable creation of the databases (more to come)
    """

    def __init__(self):
        pass

    # creation des tables
    def create_tables(self) -> None:
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

    def check_info(self, info):
        """
        check the validity of the comment passed in parameter
        """

        if type(info) is not dict:
            print(f"Error in check_info function: Parameter must be a dict")
            return {}

        if type(info["label"]) is not int:
            print(f"Error in check_info function: key 'label' must be a integer (0 or 1)")
            print("is type is: ", type(info['label']))
            return {}

        if type(info["original_topic"]) is not str:
            print(f"Error in check_info function: key 'original_topic' must be a string")
            return {}

        if type(info["comment"]) is not str:
            print(f"Error in check_info function: key 'comment' must be a string")
            return {}

        if type(info["timestamp"]) is not int:
            print(f"Error in check_info function: key 'timestamp' must be a integer")
            return {}

        return info

    def load_shows(self):
        """
        load the shows table
        """
        shows = ['adolescence',
                    'breaking_bad',
                    'the_crown',
                    'the_100',
                    'oppenheimer',
                    'wednesday',
                    'peaky_blinders',
                    'stranger_things',
                    'supernatural',
                    'euphoria'
                ]
        with engine.connect() as connection:
            for show in shows:
                db = session
                showTable = Shows(name=show)
                db.add(showTable)
                db.commit()
                db.close()

    def load_to_db(self, info):
        """
        save info to db
        """

        with engine.connect() as connection:

            check_shows = select(Shows).limit(1)
            result = connection.execute(check_shows)
            first_row = result.first()

        if first_row is None:
            self.load_shows()

        info = self.check_info(info)

        if info == {}:
            print("Error in load_to_db: Bad parameter")
            return

        try:

            with engine.connect() as connection:
                actual_show_id = session.query(Shows).filter_by(name=info["original_topic"]).first()

                if actual_show_id is None:
                    print("Error in check_info: Topic not found")
                    return
            
            with engine.connect() as connection:
                db = session
                reviewTable = Reviews(show_id=actual_show_id.show_id, review=info["comment"], label=info["label"], created_at=info["timestamp"])
                db.add(reviewTable)
                db.commit()
                db.close()

        except Exception as e:
            print(f"Error in load_to_db function: {e}")