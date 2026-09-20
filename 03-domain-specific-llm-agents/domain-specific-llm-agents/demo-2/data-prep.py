import pandas as pd
import numpy as np
import re
from datetime import datetime

# Define file path
file_path = 'dcgm.csv'  # Ensure this file is in the same directory

# ========================
# Step 1: Load the Dataset
# ========================
print("🔹 Step 1: Loading dataset...")

# Load the dataset from CSV file
# This file contains GPU usage metrics, including power, memory, and execution time.
try:
    dataset = pd.read_csv(file_path)
    print(" Dataset loaded successfully.\n")
except FileNotFoundError:
    print(f" Error: {file_path} not found. Ensure the file is in the correct directory.")
    exit()

# Display dataset structure
print("Initial Dataset Information:")
print(dataset.info())
print("\n First few rows of the dataset:")
print(dataset.head())

# ===========================
# Step 2: Clean the Dataset
# ===========================
print("\n🔹 Step 2: Cleaning dataset...")

# Handle missing values by replacing NaN with 0
dataset.fillna(0, inplace=True)

# Remove duplicate rows
dataset.drop_duplicates(inplace=True)

# Drop unnecessary columns (gpu_id is redundant)
columns_to_drop = ['gpu_id']
if 'gpu_id' in dataset.columns:
    dataset.drop(columns=columns_to_drop, inplace=True)

# Display cleaned dataset info
print(" Dataset cleaned successfully.\n")
print(" Dataset Information After Cleaning:")
print(dataset.info())

# ===========================
# Step 3: Format the Dataset
# ===========================
print("\n🔹 Step 3: Formatting dataset...")

# Convert execution time columns to float for numerical operations
if 'totalexecutiontime_sec' in dataset.columns:
    dataset['totalexecutiontime_sec'] = dataset['totalexecutiontime_sec'].astype(float)

# Convert all numerical columns to float32 to optimize memory usage
numeric_columns = dataset.select_dtypes(include=['int64', 'float64']).columns
dataset[numeric_columns] = dataset[numeric_columns].astype('float32')

# Display formatted dataset info
print(" Dataset formatted successfully.\n")
print(" Dataset Information After Formatting:")
print(dataset.info())

# ===========================
# Step 4: Annotate the Dataset
# ===========================
print("\n🔹 Step 4: Annotating dataset...")

# Categorize GPU utilization into Idle, Low, Medium, or High
def annotate_utilization(value):
    if value > 80:
        return "High"
    elif value > 50:
        return "Medium"
    elif value > 20:
        return "Low"
    else:
        return "Idle"

# Apply annotation function
if 'avgsmutilization_pct' in dataset.columns:
    dataset['gpu_utilization_category'] = dataset['avgsmutilization_pct'].apply(annotate_utilization)

# Display annotated dataset
print(" Dataset annotation completed.\n")
print(" Dataset After Annotation:")
print(dataset.head())

# ===========================
# Step 5: Save the Dataset
# ===========================
print("\n🔹 Step 5: Saving the prepared dataset...")

# Define output file
output_file = 'prepared_dcgm.csv'

# Save the cleaned and formatted dataset
dataset.to_csv(output_file, index=False)

print(f" Prepared dataset saved as '{output_file}'.\n")

