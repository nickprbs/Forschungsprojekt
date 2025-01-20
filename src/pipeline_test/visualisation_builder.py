import xarray as xa             # Used to handle .nc files
import dask.dataframe as dd
import altair as alt            # Vega Altair to visualize data
from vega_datasets import data  # Data used for vega visualization
import webbrowser               # Access to browser
import os                       # Access to file system
from dask.distributed import Client, LocalCluster
import csv

def setup_dask():
    cluster = LocalCluster(memory_limit="4GB", local_directory="./src/pipeline_test/dask_temp")
    client = Client(cluster)
    print(client)
    return client


def create_csv_dataset(client, name):
    
    
    # Lade das Dataset mit Dask-Chunks
    dataset_raw = xa.open_dataset("../monthly_avg_2015_2099.nc", chunks={"time": 50})
    print("Dataset loaded successfully:")
    print(dataset_raw)
    print("\n")

    # Konvertiere direkt zu Dask-DataFrame
    dataset_dd = dataset_raw.to_dask_dataframe()
    print(f"Initial number of rows: {len(dataset_dd)}")

    # Entferne NaN-Werte in der Spalte 'tas'
    dataset_dd_clean = dataset_dd.dropna(subset=["tas"])
    print(f"Number of rows after cleaning: {len(dataset_dd_clean)}")

    # Schreibe die Daten in CSV-Dateien (partitioniert)
    output_dir = "csv_output"
    os.makedirs(output_dir, exist_ok=True)
    dataset_dd_clean.to_csv(os.path.join(output_dir, "data_subset_*.csv"), index=False, compute=True)
    print("Dataset successfully converted to CSV files.")
    output_path = os.path.join("./src/pipeline_test/datasets", f"{name}.csv")
    combine_csv_files("./csv_output", output_path)
    
    
def combine_csv_files(input_dir, output_file):
    
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_file, exist_ok=True)
        
    if os.path.exists(output_file):
        raise OSError("dataset with this name already exists")
    
    csv_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
    
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
    
    
     
    
def build_visualization(dataset_path):
    # Load world map
    source = alt.topo_feature(data.world_110m.url, 'countries')

    # create map
    map_chart = alt.Chart(source, width=800, height=500).mark_geoshape(
        fill='lightgray',
        stroke='gray'
    ).project(type='equalEarth')

    # link to external dataset
    points_chart = alt.Chart(f"{dataset_path}.csv").mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.Size('tas:Q', title='Surface Air Temperature (tas)'),
        color=alt.Color('tas:Q', scale=alt.Scale(scheme='reds'), title='Temperature (tas)'),
        tooltip=['latitude', 'longitude', 'tas']
    )

    # Kombiniere die Karte und die Punkte
    final_chart = map_chart + points_chart

    # Exportiere das Vega-Lite JSON
    final_chart.save("./src/pipeline_test/visualization.json")
    
def open_in_browser():
    html_file = "visualization_render.html"
    html_path = os.path.abspath(html_file)
    
    webbrowser.open(f"file://{html_path}")

def main():
    
    # Get user input
    
    print("Do you want to create a new csv dataset?")
    csv_creation = str(input("y/n" + "\n"))
    while csv_creation != 'y' and csv_creation !='n':
        print("please type 'y' for yes or 'n' for no")
        csv_creation = str(input("y/n" + "\n"))
        
    csv_creation = True if csv_creation == 'y' else False
    print("Do you want to generate a new visualization JSON?")
    generate_json = str(input("y/n"+ "\n"))
    while generate_json != 'y' and generate_json !='n':
        print("please type 'y' for yes or 'n' for no")
        generate_json = str(input("y/n" + "\n"))
    generate_json = True if generate_json == 'y' else False
    
    if(csv_creation):
        #name = str(input("Please enter the name of the dataset\n"))
        print("Creating csv dataset...")
        #client = setup_dask()
        create_csv_dataset(client, "test.csv")
    if(generate_json):
        if (not create_csv_dataset):
            name = str(input("Please enter the name of the dataset\n"))
        print("building visualization...")
        build_visualization(name)
    
    # open visualization in webbrowser
    open_in_browser()
    


#run code
if __name__ == '__main__':
    output_path = os.path.join("./src/pipeline_test/datasets", "test.csv")
    combine_csv_files("./csv_output", output_path)
    build_visualization(output_path)
    open_in_browser()
    #main()