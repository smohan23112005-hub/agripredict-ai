"""
ML Crop Suitability Model — Train and predict crop recommendations.
Uses a Random Forest classifier trained on a synthetic dataset based on
realistic agricultural parameters for Andhra Pradesh crops.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "crop_suitability_rf.joblib")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")


def generate_training_data(n_samples=2000):
    """
    Generate synthetic training data for crop suitability.
    Based on realistic ranges for AP crops.
    """
    np.random.seed(42)

    crops_config = {
        "Rice": {"temp": (22, 32), "rain": (1000, 2000), "humidity": (70, 90), "ph": (5.5, 7.0), "soils": [0, 1, 3]},
        "Groundnut": {"temp": (25, 35), "rain": (500, 1200), "humidity": (50, 75), "ph": (5.5, 7.5), "soils": [2, 4, 3]},
        "Cotton": {"temp": (25, 35), "rain": (600, 1500), "humidity": (50, 70), "ph": (6.0, 8.0), "soils": [1, 2, 0, 3]},
        "Maize": {"temp": (21, 32), "rain": (500, 1200), "humidity": (55, 80), "ph": (5.5, 7.5), "soils": [3, 0, 2, 1]},
        "Red Gram": {"temp": (25, 35), "rain": (350, 1000), "humidity": (40, 70), "ph": (6.0, 7.5), "soils": [2, 1, 3, 4]},
        "Bengal Gram": {"temp": (15, 28), "rain": (200, 600), "humidity": (30, 60), "ph": (6.0, 8.0), "soils": [1, 3, 2]},
        "Sunflower": {"temp": (22, 30), "rain": (400, 900), "humidity": (45, 70), "ph": (6.0, 7.5), "soils": [1, 2, 3, 0]},
        "Chilli": {"temp": (22, 32), "rain": (500, 1200), "humidity": (55, 75), "ph": (6.0, 7.0), "soils": [3, 1, 2, 0]},
        "Jowar": {"temp": (25, 35), "rain": (300, 900), "humidity": (40, 65), "ph": (6.0, 8.0), "soils": [1, 2, 4, 3]},
        "Black Gram": {"temp": (25, 35), "rain": (400, 900), "humidity": (50, 75), "ph": (5.5, 7.5), "soils": [1, 2, 3, 0]},
    }

    # Soil encoding: 0=alluvial, 1=black, 2=red, 3=loamy, 4=sandy, 5=clayey
    records = []
    per_crop = n_samples // len(crops_config)

    for crop_name, config in crops_config.items():
        for _ in range(per_crop):
            temp = np.random.uniform(*config["temp"])
            rain = np.random.uniform(*config["rain"])
            humidity = np.random.uniform(*config["humidity"])
            ph = np.random.uniform(*config["ph"])
            soil = np.random.choice(config["soils"])
            # Season: 0=kharif, 1=rabi, 2=zaid
            if crop_name in ["Bengal Gram"]:
                season = 1
            elif crop_name in ["Red Gram", "Cotton"]:
                season = 0
            else:
                season = np.random.choice([0, 1])

            records.append({
                "temperature": round(temp, 1),
                "rainfall": round(rain, 1),
                "humidity": round(humidity, 1),
                "ph": round(ph, 1),
                "soil_type": soil,
                "season": season,
                "crop": crop_name,
            })

    df = pd.DataFrame(records)
    return df


def train_model():
    """Train the crop suitability model."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = generate_training_data(3000)

    # Features and target
    feature_cols = ["temperature", "rainfall", "humidity", "ph", "soil_type", "season"]
    X = df[feature_cols].values
    y = df["crop"].values

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)

    # Save
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)

    metrics = {
        "model_type": "Random Forest Classifier",
        "n_estimators": 100,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(accuracy, 4),
        "features": feature_cols,
        "classes": list(le.classes_),
        "classification_report": report,
        "dataset_source": "Synthetic data based on AP crop agronomic requirements",
        "limitations": [
            "Trained on synthetic data - not validated against real field outcomes",
            "Does not account for micro-climate variations",
            "Soil chemistry beyond pH is not considered",
            "Market and economic factors are not included",
        ],
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"[OK] Model trained. Accuracy: {accuracy:.4f}")
    print(f"     Model saved to: {MODEL_PATH}")

    return metrics


def predict_crop(temperature, rainfall, humidity, ph, soil_type, season):
    """Predict crop suitability using the trained model."""
    if not os.path.exists(MODEL_PATH):
        print("[WARN] Model not found. Training now...")
        train_model()

    model = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)

    # Soil encoding
    soil_map = {"alluvial": 0, "black": 1, "red": 2, "loamy": 3, "sandy": 4, "clayey": 5, "laterite": 2, "unknown": 3}
    season_map = {"kharif": 0, "rabi": 1, "zaid": 2, "annual": 0}

    soil_encoded = soil_map.get(soil_type.lower(), 3)
    season_encoded = season_map.get(season.lower(), 0)

    X = np.array([[temperature, rainfall, humidity, ph, soil_encoded, season_encoded]])

    # Predict probabilities
    proba = model.predict_proba(X)[0]
    classes = le.classes_

    # Sort by probability
    sorted_idx = np.argsort(proba)[::-1]
    predictions = []
    for idx in sorted_idx[:5]:
        predictions.append({
            "crop": classes[idx],
            "probability": round(float(proba[idx]) * 100, 1),
        })

    return predictions


if __name__ == "__main__":
    metrics = train_model()
    print(json.dumps(metrics, indent=2))
