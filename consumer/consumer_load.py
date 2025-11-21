import json
import psycopg2
import os
import time
from psycopg2 import sql

# Configuration du fichier de données
INPUT_FILE = "commentaires_labellises.json"

# Configuration de la Base de Données PostgreSQL (À MODIFIER AVEC VOS INFOS)
DB_CONFIG = {
    'dbname': 'votre_nom_de_bdd',
    'user': 'votre_utilisateur',
    'password': 'votre_mot_de_passe',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erreur de connexion à la base de données: {e}")
        sys.exit(1)

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                original_topic VARCHAR(255),
                comment TEXT,
                timestamp BIGINT,
                label VARCHAR(100)
            );
        ''')
        conn.commit()
        print("Table PostgreSQL 'comments' prête.")
    except Exception as e:
        print(f"Erreur lors de la création de la table: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_data_into_db_transactional():
    """
    Lit le fichier JSON Lines, insère les données dans Postgres en mode transactionnel.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Le fichier source {INPUT_FILE} n'existe pas encore. En attente...")
        return 0

    data_to_insert = []
    try:
        with open(INPUT_FILE, 'r') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    data_to_insert.append((
                        record['original_topic'],
                        record['comment'],
                        record['timestamp'],
                        record['label']
                    ))
                except json.JSONDecodeError:
                    print(f"Erreur de décodage JSON sur une ligne: {line.strip()}")
    except IOError as e:
        print(f"Erreur de lecture du fichier: {e}")
        return 0

    if not data_to_insert:
        os.remove(INPUT_FILE) 
        print("Aucune donnée à insérer. Fichier vide supprimé.")
        return 0

    conn = get_db_connection()
    cursor = conn.cursor()
    inserted_count = 0

    try:
        # --- DÉBUT DE LA TRANSACTION ---
        insert_query = """
            INSERT INTO comments (original_topic, comment, timestamp, label) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data_to_insert)
        
        # Si aucune erreur, on valide l'ensemble du lot
        conn.commit() 
        inserted_count = cursor.rowcount
        print(f"Transaction réussie: Insertion de {inserted_count} enregistrements dans Postgres.")

        # Si le commit réussit, on supprime le fichier source
        os.remove(INPUT_FILE)
        print(f"Fichier source {INPUT_FILE} supprimé.")

    except Exception as e:
        # Si une erreur survient, tout est annulé
        conn.rollback() 
        print(f"Erreur de transaction détectée. Rollback effectué. Erreur: {e}")

    finally:
        cursor.close()
        conn.close()
    
    return inserted_count

# Lancement
if __name__ == "__main__":
    setup_database()
    print("Démarrage du script d'insertion PostgreSQL...")
    while True:
        insert_data_into_db_transactional()
        time.sleep(5) # Vérifie le fichier toutes les 5 secondes
