import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
df = pd.read_csv('data/Machine_Maintenance_Dataset.csv')

# Features and target
X = df.drop('MachineStatus', axis=1)
y = df['MachineStatus']

# Encode target labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Save encoder
joblib.dump(encoder, "model/encoder.pkl")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
with open('model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

# Evaluation
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred, target_names=encoder.classes_))

# Save trained model
with open('model/trained_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\n✅ Model, scaler, and encoder saved successfully.")
