from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data import Reviews, Shows
from data import db

app = Flask(__name__)



db = db()


@app.route('/reviews', methods=['GET'])
def get_reviews():

    try:
        reviews = db.get_reviews()
        
        result = []
        for review in reviews:
            result.append({
                'show_id': review.show_id,
                'review_id': review.review_id,
                'review': review.review,
                'label': review.label,

            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/shows', methods=['GET'])
def get_shows():

    try:
        shows = db.get_shows()
        

        result = []
        for show in shows:

            result.append({
                'show_id': show.show_id,
                'name': show.name,
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


# @app.route('/messages', methods=['GET'])
# def get_all_messages():
#     session = Session()

#     try:
#         messages = session.query(Message).all()

#         result = []
#         for message in messages:
#             result.append({
#                 'message_id': message.message_id,
#                 'content': message.content,
#                 'channel_id': message.channel_id
#             })

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         session.close()


# @app.route('/messages/<message_id>', methods=['GET'])
# def get_message_by_id(message_id):
#     session = Session()

#     try:
#         message = session.query(Message).filter(Message.message_id == message_id).first()

#         if not message:
#             return jsonify({'error': 'Message not found'}), 404

#         result = {
#             'message_id': message.message_id,
#             'content': message.content,
#             'channel_id': message.channel_id
#         }

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         session.close()


# @app.route('/replies', methods=['GET'])
# def get_all_replies():
#     session = Session()

#     try:
#         replies = session.query(Reply).all()

#         result = []
#         for reply in replies:
#             result.append({
#                 'reply_id': reply.reply_id,
#                 'content': reply.content,
#                 'message_id': reply.message_id
#             })

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         session.close()


# @app.route('/replies/<reply_id>', methods=['GET'])
# def get_reply_by_id(reply_id):
#     session = Session()

#     try:
#         reply = session.query(Reply).filter(Reply.reply_id == reply_id).first()

#         if not reply:
#             return jsonify({'error': 'Reply not found'}), 404

#         result = {
#             'reply_id': reply.reply_id,
#             'content': reply.content,
#             'message_id': reply.message_id
#         }

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         session.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Démarrage du serveur Flask...")
    print("API disponible sur: http://localhost:5000")
    print("\nRoutes disponibles:")
    print("  GET /shows")
    print("  GET /reviews")
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur\n")

    app.run(debug=True, port=5000)