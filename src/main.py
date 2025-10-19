from gemini_vision import process_tire_images
from test_predictions import predict_strategy, reverse_engineer_meta_data
from pathlib import Path
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


fetch_lock = False

def cron_job():
    global fetch_lock
    if fetch_lock:
        return
    fetch_lock = True
    process_tire_images()
    print("Tire images processed successfully")

    for lap_file in Path("output").glob("*.json"):
        with open(lap_file, 'r') as f:
            data = json.load(f)
        lap_number = int(lap_file.stem.split("_")[1])
        print("Data: ", data)
        print("Tyre pressure: ", data.get("tyre_pressure"))
        if "tyre_pressure" not in data:
            result = reverse_engineer_meta_data(data, lap_number)
            data.update(result)
            print("Reversed engineereed data: ", data)
        else:
            print("Reversed engineereed data already exists: ", data)
        
        if "strategy" not in data:
            result = predict_strategy(data)
            print(result)
            data.update({"strategy": result["strategy"]})
            with open(lap_file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            print("Strategy already exists: ", data)
    collection_ref = db.collection('laps')
    docs = collection_ref.stream()
    for doc in docs:
        doc.reference.delete()
    for lap_file in Path("output").glob("*.json"):
        with open(lap_file, 'r') as f:
            data = json.load(f)
        lap_number = int(lap_file.stem.split("_")[1])
        collection_ref.document(f"lap_{lap_number}").set(data)
    fetch_lock = False