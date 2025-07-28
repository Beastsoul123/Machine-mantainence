# print_features.py

import os
import pickle

# point to your scaler file
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
scaler    = pickle.load(open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb'))

# show what features it expects
print("Scaler expects features in this exact order:")
for f in scaler.feature_names_in_:
    print("  -", f)
