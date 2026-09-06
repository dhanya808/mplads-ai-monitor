"""
MPLADS AI Monitor Launcher
Initializes data generation, trains/executes the AI ML anomaly engine,
and launches the Streamlit interface.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.dataset_generator import generate_mplads_dataset
from backend.ml_engine import process_mplads_anomalies

def setup():
    print("=" * 60)
    print("🏛️  MPLADS AI Monitor | MoSPI DIID")
    print("AI-Powered Anomaly, Fraud & Inefficiency Monitoring Platform")
    print("=" * 60)
    
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    processed_csv = os.path.join(data_dir, "mplads_processed.csv")
    
    print("[1/3] Synthesizing realistic multi-constituency MPLADS records...")
    raw_df = generate_mplads_dataset(num_records=200)
    
    print("[2/3] Executing AI/ML Anomaly Engine (NLP, Cost Outliers, Delays)...")
    processed_df = process_mplads_anomalies(raw_df)
    processed_df.to_csv(processed_csv, index=False)
    print(f"      ✓ {len(processed_df)} projects scored & cached at: {processed_csv}")
    
    print("[3/3] Launching Government Command Center Interface on localhost:8501...")
    cmd = [sys.executable, "-m", "streamlit", "run", os.path.join(BASE_DIR, "app.py"), "--server.port=8501", "--server.headless=true"]
    subprocess.run(cmd)

if __name__ == "__main__":
    setup()
