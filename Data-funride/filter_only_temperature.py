import pandas as pd

# Load dataset from CSV file
input_csv_path = r"C:\Forschungs-Projekt-Daten\filtered_climate_data.csv"
output_csv_path = r"C:\Forschungs-Projekt-Daten\filtered_climate_data_01-01-2015"

# Define the chunk size
chunk_size = 100000  # Adjust the chunk size as needed
chunk_no = 0
# Process the data in chunks
header_written = False
for chunk in pd.read_csv(input_csv_path, chunksize=chunk_size):
    chunk_no += 1
    # Filter out rows where the "temperature" column is empty
    filtered_chunk = chunk[chunk['Time'] == '2015-01-31']

    
    # Write the filtered chunk to the output CSV file
    if not header_written:
        filtered_chunk.to_csv(output_csv_path, index=False, mode='w')
        header_written = True
    else:
        filtered_chunk.to_csv(output_csv_path, index=False, mode='a', header=False)

    print(f"Processed and saved chunk number {chunk_no} with {len(filtered_chunk)} rows")


print(f"Filtered data saved to {output_csv_path}")