import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def generate_reference_data(n_samples=1000):
    """ Recreates the baseline data distribution the model was trained on. """
    np.random.seed(42)
    amounts = np.random.uniform(5.0, 3000.0, n_samples)
    is_intl = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])
    return pd.DataFrame({'amount': amounts, 'is_international': is_intl})

def generate_drifted_production_data(n_samples=1000):
    """ 
    Simulates live production data where consumer behavior has shifted. 
    Amounts are drastically higher, and international volume spiked.
    """
    np.random.seed(99)
    # Drift 1: Transaction amounts shifted from max $3000 to max $5000
    amounts = np.random.uniform(500.0, 5000.0, n_samples)
    # Drift 2: International transactions jumped from 15% to 40%
    is_intl = np.random.choice([0, 1], size=n_samples, p=[0.60, 0.40])
    return pd.DataFrame({'amount': amounts, 'is_international': is_intl})

print("Generating Reference (Training) Data...")
reference_data = generate_reference_data()

print("Generating Current (Production) Data with intentional drift...")
current_data = generate_drifted_production_data()

print("Executing Evidently AI Data Drift Analysis...")
# Initialize the Evidently report with the Data Drift preset
drift_report = Report(metrics=[DataDriftPreset()])

# Calculate the statistical drift between the two datasets
drift_report.run(reference_data=reference_data, current_data=current_data)

# Save the output as a standalone interactive web dashboard
report_path = "evidently_drift_report.html"
drift_report.save_html(report_path)

print(f"Drift analysis complete! Dashboard saved locally as: {report_path}")