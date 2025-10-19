# F1 Tyre Strategizer

A computer-vision and ML-powered tool to infer tyre condition from track-side images and recommend optimal pit/tyre strategies in real-time.

## Features
- Predicts strategy using two ML models (Random Forest and Decision Tree)
  - Runs both models concurrently and returns the better result per prediction
- Vision-assisted metadata extraction from tyre images (Gemini Vision)
- Reverse-engineering of missing sensor metrics from visual cues
- Firestore sync for laps and predictions
- Scripts for training, testing, and scheduled processing

## Project Structure
```
F1-Tyre-Strategizer/
  data/
    generated/
      edge_cases.csv
      f1_tire_data.csv
  models/
    dt_model.pkl
    feature_columns.pkl
    label_encoders.pkl
    metadata.pkl
    rf_model.pkl
  output/                    # lap JSONs written here (when running from repo root)
  src/
    data_generation.py
    gemini_vision.py
    inspect_data.py
    main.py
    monitor_tire_images.py
    pi_api_client.py
    test_predictions.py
    track_strategy.py
    train_model.py
    output/                  # lap JSONs when running scripts from src/
    tire_images/
      lap_1/ ...             # example images used by gemini_vision
      logs/
  requirements.txt
  service.json               # Firebase Admin SDK service account (see setup)
```

## Requirements
- Windows 10/11 with PowerShell 7+ (repo is Windows-friendly)
- Python 3.11 (recommended to match the existing `venv`)
- Google Firebase project (Firestore), service account JSON
- Gemini API access (for `gemini_vision.py`) if you plan to use image processing

## Quick Start (Local)
1) Create and activate venv (optional if you’ll reuse `venv/`):
```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

2) Install dependencies:
```powershell
pip install -r requirements.txt
```

3) Place your Firebase service account file at project root as `service.json`.

4) Train models (creates files in `models/`):
```powershell
python src/train_model.py
```
You should see `models/rf_model.pkl`, `models/dt_model.pkl`, `models/label_encoders.pkl`, `models/feature_columns.pkl`, and `models/metadata.pkl` created.

5) Run a quick prediction (interactive tester):
```powershell
python src/test_predictions.py
```
- `test_predictions.predict_strategy(tire_data)` builds features, runs RF and DT concurrently, and returns the better one using weighted score (accuracy × confidence).

## Using The Predictor From Your Code
Minimal example:
```python
from test_predictions import predict_strategy

sample = {
    'compound': 'soft',
    'lap_number': 15,
    'wear_pattern': 'even',
    'sidewall_deformation': False,
    'tyre_pressure': 20.6,
    'is_graining': False,
    'tyre_temperature': 102,
    'track_temperature': 28,
}
result = predict_strategy(sample)
print(result)  # { 'strategy': ..., 'confidence': ..., 'risk_score': ..., 'lap_percentage': ... }
```
Notes:
- The function concurrently infers predictions from Decision Tree and Random Forest and returns whichever scores better using (model_accuracy × model_confidence).
- It relies on artifacts in `models/` and the encoders/feature ordering trained by `src/train_model.py`.

## Image Processing (Gemini Vision)
- `src/gemini_vision.py` processes images placed under `src/tire_images/<lap_x>/...` and produces per-lap JSONs in `src/output/` when executed from `src/`.
- These JSONs can then be augmented with reverse-engineered telemetry by `reverse_engineer_meta_data` and fed into `predict_strategy`.
- Ensure your Gemini API configuration is set inside `gemini_vision.py` or via environment variables, depending on how you’ve integrated it.

## Firestore Sync
- `src/main.py` loads `../service.json` (relative to `src/`) and writes lap documents to Firestore.
- To run the scheduled image processing + Firestore push flow, you can invoke `cron_job()` or adapt it into your own scheduler. Example:
```powershell
python -c "from src.main import cron_job; cron_job()"
```
Ensure your Firestore rules and service account permissions allow read/write to the `laps` collection.

## Data Generation and Training
- Generate data or inspect datasets:
  - `src/data_generation.py` (if you want to synthesize more samples)
  - `src/inspect_data.py` for EDA or quick checks
- Train models:
  - `src/train_model.py` handles label encoding, feature engineering, training DT/RF, and saving artifacts + metadata (accuracies, feature names)

## Common Commands
```powershell
# Activate venv
./venv/Scripts/Activate.ps1

# Install deps
pip install -r requirements.txt

# Train
python src/train_model.py

# Test a prediction
python src/test_predictions.py

# Process images and push to Firestore (via cron_job)
powershell -Command "python -c \"from src.main import cron_job; cron_job()\""
```

## Configuration
- `service.json`: Firebase Admin SDK service account file at project root (referenced by `src/main.py` as `../service.json` when run from `src/`).
- Gemini API: configure in `src/gemini_vision.py` (env vars or inline config depending on your setup).

## Troubleshooting
- Module import errors when running from `src/`:
  - Prefer running scripts with `python src/<script>.py` from the project root so relative paths resolve as expected.
- `FileNotFoundError` for models or encoders:
  - Ensure `python src/train_model.py` has been run and `models/` contains all required `.pkl` files.
- Firestore permission errors:
  - Verify `service.json` is valid and has permissions; check Firestore rules and project ID.
- Gemini API errors:
  - Confirm API key/credentials and that images exist under `src/tire_images/<lap_x>/`.
- Different `output/` locations:
  - When running from project root, output defaults to `output/`.
  - When running from within `src/`, many scripts write to `src/output/`.

## Contributing
- Create a feature branch, commit your changes, and open a PR.
- For experiments, prefer local branches (e.g., `multi-threading`) to avoid altering `main`.

## License
MIT (or your chosen license). Update this section as appropriate.
