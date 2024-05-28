from confluent_kafka import Consumer, KafkaError
import json
from pymongo import MongoClient

# Initialize the Consumer for TMDb
tmdb_consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'tmdb-group',
    'auto.offset.reset': 'earliest'
})

# Initialize the Consumer for Musixmatch
musixmatch_consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'musixmatch-group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the topics
tmdb_consumer.subscribe(['movies_topic'])
musixmatch_consumer.subscribe(['music_topic'])

# Initialize MongoDB Client
client = MongoClient('mongodb://localhost:27017/')
db = client['ProyectoCPYD']
tmdb_collection = db['movies']
musixmatch_collection = db['music']

try:
    while True:
        # Poll for TMDb messages
        tmdb_msg = tmdb_consumer.poll(1.0)
        if tmdb_msg is not None:
            if tmdb_msg.error():
                if tmdb_msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f'{tmdb_msg.topic()} [{tmdb_msg.partition()}] reached end at offset {tmdb_msg.offset()}')
                else:
                    raise KafkaError(tmdb_msg.error())
            else:
                tmdb_data = json.loads(tmdb_msg.value().decode('utf-8'))
                print(f"Received TMDb message: {tmdb_data}")
                # Insert TMDb data into MongoDB
                tmdb_collection.insert_one(tmdb_data)
        
        # Poll for Musixmatch messages
        musixmatch_msg = musixmatch_consumer.poll(1.0)
        if musixmatch_msg is not None:
            if musixmatch_msg.error():
                if musixmatch_msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f'{musixmatch_msg.topic()} [{musixmatch_msg.partition()}] reached end at offset {musixmatch_msg.offset()}')
                else:
                    raise KafkaError(musixmatch_msg.error())
            else:
                musixmatch_data = json.loads(musixmatch_msg.value().decode('utf-8'))
                print(f"Received Musixmatch message: {musixmatch_data}")
                # Insert Musixmatch data into MongoDB
                musixmatch_collection.insert_one(musixmatch_data)

finally:
    # Close down consumers to commit final offsets.
    tmdb_consumer.close()
    musixmatch_consumer.close()
    # Close MongoDB client
    client.close()