import altair as alt
from vega_datasets import data

#pip install altair
#pip install pandas  # For handling data
#pip install vega_datasets  # Sample datasets for experimentation
#pip install selenium altair_saver
#pip install altair-saver selenium



# Load dataset
cars = data.cars()
countries = data.countries()
# Create scatter plot
scatter_plot_cars = alt.Chart(cars).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Horsepower', 'Miles_per_Gallon']
).interactive()

scatter_plot_countries = alt.Chart(countries).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Horsepower', 'Miles_per_Gallon']
).interactive() 

# Save as HTML
scatter_plot_countries.save('.\plots\scatter_plot_countries.html')

print("Chart saved as scatter_plot.html")
