from src.gemini_vision import process_tire_images
from src.test_predictions import predict_strategy
from pathlib import Path
import json



if __name__ == "__main__":
    process_tire_images()
    print("Tire images processed successfully")

    tyre_data_list = []
    for lap_file in Path("output").glob("*.json"):
        with open(lap_file, 'r') as f:
            data = json.load(f)
        lap_number = int(lap_file.stem.split("_")[1])
        compound = "soft"
        tyre_pressure = 20.5
        tyre_temperature = 102
        track_temperature = 28
        data.update({
            "compound": compound,
            "lap_number": lap_number,
            "tyre_pressure": tyre_pressure,
            "tyre_temperature": tyre_temperature,
            "track_temperature": track_temperature
        })
        tyre_data_list.append(data)
    
    for tyre_data in tyre_data_list:
        result = predict_strategy(tyre_data)
        print(result)
