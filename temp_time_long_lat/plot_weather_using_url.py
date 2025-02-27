import altair as alt
from vega_datasets import data

source = r"https://1drv.ms/x/c/7f7e4e0b1106ffa6/EQbwEmL116BCue0n1co1PfwBiEyvmPxji1pax5LuMVC1cg?e=fZAiud"

scatter_plot_climate = alt.Chart(source).mark_circle(size=60).encode(
    x='Latitude:Q',
    y='Longitude:Q',
    color='Origin',
    tooltip=['Time', 'Latitude', 'Longitude', 'Temperature']
).interactive()

scatter_plot_climate.save(r'C:\Users\juliu\OneDrive\Desktop\Informatik_Studium\5.Semester\Bachelor Forschungsprojekt\Forschungsprojekt\Forschungsprojekt\plots\scatter_plot_climate_from_url.html')

print("Chart saved as scatter_plot_climate.html")