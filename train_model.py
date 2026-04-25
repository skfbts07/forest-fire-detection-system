import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("forest_fire_data.csv")

# Encode location names into numbers
le = LabelEncoder()
df["Location"] = le.fit_transform(df["Location"])

# Features and target
X = df[["Location", "Temperature", "Humidity", "WindSpeed", "Rainfall"]]
y = df["Fire"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoder
joblib.dump(model, "model.pkl")
joblib.dump(le, "location_encoder.pkl")

print("✅ Model trained and saved with Location feature")
