#!/usr/bin/env python3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib
import os, sys

XLSX_PATH = os.path.expanduser('~/Downloads/project_dataset.xlsx')
OUT_MODEL = os.path.expanduser('~/ros2_ws/src/smart_room_nav/config/model.pkl')

# Load dataset
try:
    df = pd.read_excel(XLSX_PATH)
except Exception as e:
    print("ERROR reading Excel file:", e)
    sys.exit(1)

features = ['Time of Day', 'Task Type', 'Room status']
target = 'Target Room'

# Encode categorical features
df_encoded = df.copy()
mappings = {}
for col in features + [target]:
    cat = df[col].astype('category')
    df_encoded[col] = cat.cat.codes
    mappings[col] = list(cat.cat.categories)

X = df_encoded[features].values
y = df_encoded[target].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = DecisionTreeClassifier(max_depth=6, random_state=42)
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(f"Model trained. Test accuracy = {acc:.3f}")

# Save model + mappings together
joblib.dump({"model": clf, "mappings": mappings},
            "/home/sparsh05/ros2_ws/src/smart_room_nav/config/model.pkl")
print("Model + mappings saved at:", OUT_MODEL)

