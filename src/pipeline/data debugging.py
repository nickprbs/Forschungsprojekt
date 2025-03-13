import pandas as pd

df = pd.read_csv('/Users/nick/Dokumente/Studium/B.Sc Informatik/24-25 WiSe/Bachelor Forschungsprojekt/Forschungsprojekt/src/datasets/yearly_avg_2015_2099_downsampled.csv')

min_lat = df["lat"].min()
max_lat = df["lat"].max()

min_lon = df["lon"].min()
max_lon = df["lon"].max()

min_tas = df["tas"].min()
max_tas = df["tas"].max()

print(f"min_lat: {min_lat}, max_lat: {max_lat}\nmin_lon: {min_lon}, max_lon: {max_lon}\nmin_tas: {min_tas}, max_tas: {max_tas}")

data_points_per_year = df.groupby('time').size()

print(f"datapoints per year: \n{data_points_per_year}")