import pandas as pd

# Load dataset from CSV file
input_csv_path = r"D:\Forschungsprojekt\filtered_climate_data.csv"
output_csv_path = r"D:\Forschungsprojekt\yearly_average_climate_data.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(input_csv_path)

# Convert 'Time' column to datetime
data['Time'] = pd.to_datetime(data['Time'])

# Extract the year from the 'Time' column
data['Year'] = data['Time'].dt.year

# Group the data by year and calculate the average temperature for each year
yearly_average = data.groupby('Year')['Temperature'].mean().reset_index()

# Save the yearly average data to a new CSV file
yearly_average.to_csv(output_csv_path, index=False)

print(f"Yearly average data saved to {output_csv_path}")