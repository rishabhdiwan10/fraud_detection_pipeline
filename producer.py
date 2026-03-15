import json
import time
import random
import uuid
from datetime import datetime
from confluent_kafka import Producer

# Kafka connection configuration matching your Docker Compose setup
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

TOPIC = 'transactions'

def delivery_report(err, msg):
    """ Callback to confirm message delivery to the Kafka cluster. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    # Commenting out the success print to avoid terminal spam, uncomment for debugging
    # else:
    #     print(f"Delivered transaction to {msg.topic()} [{msg.partition()}]")

def generate_transaction():
    """ Generates synthetic credit card transaction data. """
    # Simulating standard financial features an XGBoost model would analyze
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": f"U_{random.randint(1000, 9999)}",
        "amount": round(random.uniform(5.0, 3000.0), 2),
        "merchant_id": f"M_{random.randint(100, 999)}",
        "timestamp": datetime.utcnow().isoformat(),
        # A simple feature flag to simulate higher risk transactions
        "is_international": random.choices([0, 1], weights=[0.85, 0.15])[0] 
    }

print(f"Initiating transaction stream to Kafka topic: '{TOPIC}'...")
print("Press Ctrl+C to stop.")

try:
    while True:
        transaction = generate_transaction()
        
        # Serialize the Python dictionary to a JSON formatted string, then encode to bytes
        producer.produce(
            TOPIC, 
            value=json.dumps(transaction).encode('utf-8'), 
            callback=delivery_report
        )
        
        # Serve delivery callback queue
        producer.poll(0) 
        
        # Pushing ~3 transactions per second to simulate real-time load
        time.sleep(0.33) 
        
except KeyboardInterrupt:
    print("\nInterrupt received. Shutting down stream...")
finally:
    # Ensure all remaining messages in the queue are sent before closing
    print("Flushing final messages to Kafka...")
    producer.flush()
    print("Stream stopped cleanly.")