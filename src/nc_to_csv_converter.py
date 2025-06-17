import time
import xarray as xa                                 # Used to handle .nc files
import dask.dataframe as dd                         # Effitiently load big data files
from dask.distributed import Client, LocalCluster   # Process data in parallel
import os                                           # Access to file system
import csv
import shutil

def setup_dask():
    """
    Performs several Dask setup steps
    """
    os.makedirs("./src/dask_temp", exist_ok=True)
    cluster = LocalCluster(memory_limit="4GB", local_directory="./src/dask_temp")
    client = Client(cluster)
    print(client)
    return client


def create_csv_dataset(client):
    """
    Creates a single csv file based on the selected nc file. 
    Assumes the nc files are located in the parent directory of the repository.
    The output will be written to ./src/datasets
    :param client: Dask client used for parallelization
    """
    print("Which .nc dataset would you like to use?")
    files = os.listdir("../")
    print(os.path.abspath('../'))
    nc_files = []
    # Retrieve all nc files from the parent directory of the repository
    for file in files:
        if file.endswith(".nc"):
            nc_files.append(file)
    for i, file in enumerate(nc_files):
        print(f'{i+1}): {file}')
    correct_input = False 
    while not correct_input:
        number = input("Please enter the number: \n")
        try:
            number = int(number)
            file = nc_files[number-1]
            correct_input = True
        except Exception:
            print(f"{number} is not a correct number. Please try again")
    
    # Load the dataset with dask
    dataset_raw = xa.open_dataset(f"../{file}", chunks={"time": 50})
    print("Dataset loaded successfully:")
    print(dataset_raw)
    print("\n")

    # Convert to dask dataframe
    dataset_dd = dataset_raw.to_dask_dataframe()
    print(f"Initial number of rows: {len(dataset_dd)}")

    # Remove all NaN values in column 'tas'
    dataset_dd_clean = dataset_dd.dropna(subset=["tas"])
    print(f"Number of rows after cleaning: {len(dataset_dd_clean)}")

    # Write data in csv-files (partitioned)
    output_dir = "./src/csv_output"
    os.makedirs(output_dir, exist_ok=True)
    dataset_dd_clean.to_csv(os.path.join(output_dir, "data_subset_*.csv"), index=False, compute=True)
    print("Dataset successfully converted to CSV files.")
    os.makedirs("./src/datasets", exist_ok=True)
    output_path = os.path.join("./src/datasets", f"{file.removesuffix('.nc')}.csv")
    combine_csv_files("./src/csv_output", output_path)
    
    
    
def combine_csv_files(input_dir, output_file):
    """
    Helper function to combine several csv files into a single csv file
    :param input_dir: path to the directory containing the csv files
    :param output_file: path to the location where the combined file will be written to
    """
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_file, exist_ok=True)
        
    if os.path.exists(output_file):
        raise OSError("dataset with this name already exists")
    
    csv_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
    csv_files.sort()
    
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        header_written = False
        for file in csv_files:
            with open(file, mode='r') as infile:
                reader = csv.reader(infile)
                header = next(reader)
                
                if not header_written:
                    writer.writerow(header)
                    header_written = True
                
                for row in reader:
                    writer.writerow(row)
            os.remove(file)   
            
    print(f"all files have been merged into {output_file}")
    
#run code
if __name__ == '__main__':
    try:
        client = setup_dask()
        create_csv_dataset(client)
    # Cleanup temporary directories
    finally:
        client.shutdown()
        client.close()
        shutil.rmtree('./src/csv_output', ignore_errors=True)
        shutil.rmtree('./src/dask_temp', ignore_errors=True)
        
    