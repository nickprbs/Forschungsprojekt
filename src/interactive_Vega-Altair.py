import altair as alt
import pandas as pd
import numpy as np

# Create a DataFrame with x values
x = np.linspace(-10, 10, 500)
df = pd.DataFrame({'x': x})

# Define the slider for the exponent 'a'
slider_a = alt.binding_range(min=-10.0, max=10.0, step=0.1, name='Exponent (a)')
a_param = alt.param(bind=slider_a, name='a', value=1.0)

# Define the chart with a calculated field using the parameter
plot = alt.Chart(df).transform_calculate(
    f_x='pow(datum.x, a)',  # Use `pow` for exponentiation
).encode(
    x=alt.X('x:Q', title='x'),
    y=alt.Y('f_x:Q', title='f(x)'),
).mark_line().add_params(
    a_param
).properties(
    width=1000,
    height=600
)

# Save the chart to an HTML file
plot.save('./plots/interactive_plot.html')
