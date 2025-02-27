import xarray as xr
import pandas as pd

# Load the NetCDF file
file_path = "monthly_avg_2015_2099.nc"
ds = xr.open_dataset(file_path)

# Ensure you have the right variable names for temperature, latitude, longitude, and time
temperature_var = "tas"
latitude_var = "lat"
longitude_var = "lon"
time_var = "time"

# Process data in chunks
chunk_size = 100  # Adjust the chunk size as needed
chunks = ds[temperature_var].chunk({'time': chunk_size})

# Initialize the CSV file with headers
header_written = False

# Iterate over the chunks and process the data
for time, chunk in chunks.groupby('time'):
    df_chunk = chunk.to_dataframe().reset_index()
    
    # Optional: Rename columns for clarity
    df_chunk.rename(columns={latitude_var: "Latitude", longitude_var: "Longitude", time_var: "Time", temperature_var: "Temperature"}, inplace=True)
    
    # Write the chunk to a CSV file incrementally
    df_chunk.to_csv('A:\Forschungsprojekt\climate_data.csv', mode='a', header=not header_written, index=False)
    header_written = True
    
    print(f"Processed and saved chunk for time: {time}")

print("Data processing complete.")