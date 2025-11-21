from kafka import KafkaConsumer
import pickle
import json
import time
import os
import sys

# --- Loading of model and verctorizer ---
model_path = "/home/kristen/Rendu/DATA/ML_Pool/C-DAT-300-COT-2-1-endtoendml-5/data/models/model.pkl"
vectorize_path="/home/kristen/Rendu/DATA/ML_Pool/C-DAT-300-COT-2-1-endtoendml-5/data/models/vectorized.pkl"
OUTPUT_FILE = "commentaires_labellises.json" # file that the second consumer will use


def load_utilities(path):
    """
        a function that allows you to retrieve the model and vectorizer
    """
    try:
        with open(path, "rb") as f:
            utility = pickle.load(f)
        print("Success, loading completed")
        return utility
    except Exception as e:
        print(f"Loading error: {e}")
        sys.exit(1)
        
model = load_utilities(model_path)
vectorizer = load_utilities(vectorize_path)



# --- Fonctions de Traitement ---

def predict_label(comment_text):
    """ 
        Returns the prediction of the sentiment conveyed by the comment
    """
    if not comment_text: return "NO_TEXT"
    try:
        # vectorize a text before prediction
        vector=vectorizer.transform([comment_text])
        prediction = model.predict(vector) 
        return prediction[0]  # return label predict
    except Exception as e:
        print(f"Prediction error: {e}")
        return "ERROR"



def append_to_json_file(record, filename=OUTPUT_FILE):
    """ 
        Retrieve a dictionary containing the topic, the comment, and its label, and save it to a JSON file.
    """
    mode = 'a' if os.path.exists(filename) else 'w'
    try:
        with open(filename, mode) as f:
            f.write(json.dumps(record) + '\n')
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
        
        

def consumer_realtime_to_file():
    list_of_topics = ['adolescence',
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

    
    consumer = KafkaConsumer(
        *list_of_topics,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True
    )
    
    print(f"Launch of consumer ")

    try:
        for message in consumer:
            comment_data = message.value
            title = comment_data.get('title', '')
            selftext = comment_data.get('selftext', '')
            text_to_process = f"{title} {selftext}".strip()
            timestamp = int(time.time())

            if text_to_process:
                label = str(predict_label(text_to_process))
                
                labeled_record = {
                    "original_topic": message.topic,
                    "comment": text_to_process,
                    "timestamp": timestamp,
                    "label": label
                }
                
                label_send = {
                    "original_topic": message.topic,
                    "comment": text_to_process,
                    "timestamp": timestamp,
                    "label": int(label)
                }
                
                append_to_json_file(labeled_record)
                
                print(f"Labellisé et écrit: Topic='{message.topic}', comment={text_to_process}, Label='{label}'")

                return label_send
    except KeyboardInterrupt:
        print("Stopped by the user.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consumer_realtime_to_file()