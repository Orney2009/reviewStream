import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


load_dotenv()




# def clean_html(html_text):
#     soup = BeautifulSoup(html_text, 'html.parser')
#     text = soup.get_text()
#     text = text.strip()
#     return text


# def get_teams():
#     url = os.getenv('URL_BASE')
#     access_token = os.getenv('TOKEN')

#     if not url or not access_token:
#         raise ValueError("URL_BASE et TOKEN doivent être définis dans le fichier .env")

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#     }

#     try:
#         response = requests.get(f'{url}/me/memberOf', headers=headers)

#         if response.status_code != 200:
#             print(f"Erreur API: Status code {response.status_code}")
#             return {}

#         data = response.json()
#         teams_data = data.get('value', [])

#         teams = {}
#         for team in teams_data:
#             display_name = team.get('displayName')
#             team_id = team.get('id')
#             if display_name and team_id:
#                 teams[team_id] = display_name

#         return teams

#     except requests.exceptions.ConnectionError:
#         print("Erreur: Impossible de se connecter à l'API")
#         return {}
#     except requests.exceptions.RequestException as e:
#         print(f"Erreur lors de la requête: {e}")
#         return {}


# def get_channels(team_id, headers):
#     url = os.getenv('URL_BASE')

#     try:
#         response = requests.get(f'{url}/teams/{team_id}/channels', headers=headers)

#         if response.status_code != 200:
#             print(f"Erreur API (channels): Status code {response.status_code}")
#             return []

#         data = response.json()
#         channels_data = data.get('value', [])

#         channels = []
#         for channel in channels_data:
#             channel_id = channel.get('id')
#             display_name = channel.get('displayName')
#             if channel_id and display_name:
#                 channels.append({
#                     'id': channel_id,
#                     'displayName': display_name
#                 })

#         return channels

#     except requests.exceptions.ConnectionError:
#         print("Erreur: Impossible de se connecter à l'API")
#         return []
#     except requests.exceptions.RequestException as e:
#         print(f"Erreur lors de la requête: {e}")
#         return []


# def get_messages(team_id, channel_id, headers):
#     url = os.getenv('URL_BASE')

#     try:
#         response = requests.get(
#             f'{url}/teams/{team_id}/channels/{channel_id}/messages',
#             headers=headers
#         )

#         if response.status_code != 200:
#             print(f"Erreur API (messages): Status code {response.status_code}")
#             return []

#         data = response.json()
#         messages_data = data.get('value', [])

#         messages = []
#         for message in messages_data:
#             message_id = message.get('id')
#             content = message.get('body', {}).get('content', '')
#             content_clean = clean_html(content)

#             if message_id:
#                 replies = get_replies(team_id, channel_id, message_id, headers)

#                 messages.append({
#                     'id': message_id,
#                     'content': content_clean,
#                     'replies': replies
#                 })

#         return messages

#     except requests.exceptions.ConnectionError:
#         print("Erreur: Impossible de se connecter à l'API")
#         return []
#     except requests.exceptions.RequestException as e:
#         print(f"Erreur lors de la requête: {e}")
#         return []


# def get_replies(team_id, channel_id, message_id, headers):
#     url = os.getenv('URL_BASE')

#     try:
#         response = requests.get(
#             f'{url}/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies',
#             headers=headers
#         )

#         if response.status_code != 200:
#             return []

#         data = response.json()
#         replies_data = data.get('value', [])

#         replies = []
#         for reply in replies_data:
#             reply_id = reply.get('id')
#             content = reply.get('body', {}).get('content', '')
#             content_clean = clean_html(content)

#             if reply_id:
#                 replies.append({
#                     'id': reply_id,
#                     'content': content_clean
#                 })

#         return replies

#     except requests.exceptions.ConnectionError:
#         return []
#     except requests.exceptions.RequestException as e:
#         return []


def export_to_database():

    print("Création de la base de données...")

    engine = create_engine('sqlite:///teams_data.db', echo=False)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    access_token = os.getenv('TOKEN')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    print("Récupération des équipes...")
    teams = get_teams()

    if not teams:
        print("Aucune équipe trouvée")
        session.close()
        return

    print(f"{len(teams)} équipe(s) trouvée(s)")

    for team_id, team_name in teams.items():
        print(f"\nTraitement de l'équipe: {team_name}")

        team = Team(team_id=team_id, display_name=team_name)
        session.add(team)

        channels = get_channels(team_id, headers)
        print(f"  {len(channels)} channel(s) trouvé(s)")

        for channel_data in channels:
            channel_id = channel_data['id']
            channel_name = channel_data['displayName']

            channel = Channel(
                channel_id=channel_id,
                display_name=channel_name,
                team_id=team_id
            )
            session.add(channel)

            messages = get_messages(team_id, channel_id, headers)
            print(f"    Channel '{channel_name}': {len(messages)} message(s)")

            for message_data in messages:
                message_id = message_data['id']
                message_content = message_data['content']

                message = Message(
                    message_id=message_id,
                    content=message_content,
                    channel_id=channel_id
                )
                session.add(message)

                for reply_data in message_data['replies']:
                    reply_id = reply_data['id']
                    reply_content = reply_data['content']

                    reply = Reply(
                        reply_id=reply_id,
                        content=reply_content,
                        message_id=message_id
                    )
                    session.add(reply)

    print("\nEnregistrement dans la base de données...")
    session.commit()
    session.close()

    print("Export terminé avec succès!")
    print("Base de données créée: teams_data.db")


if __name__ == "__main__":
    export_to_database()