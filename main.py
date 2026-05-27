# main.py
# Entry point - runs all modules in the correct order

import subprocess
import sys
import os

def run(script: str, description: str) -> bool:
    """Runs a Python script as a separate process. Returns True if successful."""
    print(f"{'-' * 40}")
    print(f" {description}")
    print(f"{'-' * 40}")
    
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"\n ERROR in {script} - stopping.")
        return False
    print(f"\n{description} completed.")
    return True

if __name__ == "__main__":
    # change working directory to the folder where main.py lives
    # so all relative paths (dati/, output/) work correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("output", exist_ok=True)
    
    print("\n" + "█" * 55)
    print("  AI Labor Market Impact Analysis — Start")
    print("█" * 55)
    steps = [
        ("analysis/cleaning_eda.py",   "Task 1 — Data Cleaning & EDA"),
        ("analysis/sql_analysis.py",   "Task 2 — SQL Analysis"),
        ("analysis/visualization.py",  "Task 3 — Visualization"),
        ("analysis/ml_model.py",       "Task 4 — Machine Learning Model"),
    ]
    
    for script, description in steps:
        ok = run(script, description)
        if not ok:
            sys.exit(1)
            
    print("\n" + "█" * 55)
    print("  All tasks completed successfully!")
    print("  Charts and results saved to: output/")
    print("█" * 55 + "\n")