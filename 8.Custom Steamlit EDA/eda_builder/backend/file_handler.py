# Handles CSV uploads and sample dataset loading

import pandas as pd
import os

SAMPLE_DATASETS = {
    "Titanic": "titanic.csv",
    "Iris": "iris.csv",
    "Wine Quality": "winequality.csv",
    "Tips": "tips.csv",
    "Diabetes": "diabetes.csv"
}

SAMPLE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_data")

def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        return None

def load_sample(name):
    fname = SAMPLE_DATASETS.get(name)
    if not fname:
        return None
    path = os.path.join(SAMPLE_DATA_PATH, fname)
    if not os.path.exists(path):
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        return None 