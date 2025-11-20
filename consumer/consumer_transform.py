from kafka import KafkaConsumer, KafkaProducer
import pickle
import json
import pandas as pd


model_path="/home/kristen/Rendu/DATA/ML_Pool/C-DAT-300-COT-2-1-endtoendml-5/modele_labellisation.pkl"

def load_model(path=model_path):
    """
        this fonction allows you to retrieve the created model
    """
    with open(path, "rb") as f:
        model = pickle.load(f)
    print("Success, model loaded.")
    return model

def consumer_transform():
    comments=[]
    list_of_topics=['adolescence',
                    'death_of_unicorn',
                    'grey_anatomy',
                    'la_casa_del_papel',
                    'le_parrain',
                    'wednesday',
                    'peaky_blinders',
                    'stranger_things',
                    'supernatural',
                    'topic_brut',
                    'you',
                ]
    
    try:
    
        for topic in list_of_topics:
            consumer = KafkaConsumer(
            topic,
            bootstrap_servers="localhost:9092",
            auto_offset_reset="earliest",
            value_deserializer=lambda v: json.loads(v.decode("utf-8"))  # JSON obligatoire
            )
            # print(type(consumer))
            for comment in consumer:
                print(f'Actual topic : {topic}')
                comments.append(comment.value)
                # appliquer la fonction de prédiction au comment
                #   label = predict_label(comment)
                #    print(f"Predition : {label}")
                # results_prediction = {"topic": topic, "label": label}
                # return results_prediction
    
    except Exception as e:
        print(f" Erreur lors de la prédiction : {e}")
           
            
# Lancement
if __name__ == "__main__":
    consumer_transform() 