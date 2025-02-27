import pandas as pd

# Load dataset from CSV file
data = pd.read_csv(r"A:\Forschungsprojekt\filtered_climate_data.csv")

# Count the number of rows in the DataFrame
num_rows = len(data)

print(f"Number of rows: {num_rows}")