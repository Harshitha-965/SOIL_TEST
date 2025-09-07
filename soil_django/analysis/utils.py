# analysis/utils.py

import os
import pandas as pd

def load_csv_data(file_name):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
    return pd.read_csv(file_path)