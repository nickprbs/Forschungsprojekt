"""
Pipeline test assuming the following steps:
1. Load data 
2. build visualization using altair
3. export json
4. show visualization
"""
import os
import altair as alt
import pandas as pd
import geopandas as gpd
from vega_datasets import data

if __name__== '__main__':
    
    # load data
    gdf_quakies = gpd.read_file(data.earthquakes.url, driver="GeoJSON")
    gdf_world = gpd.read_file(data.world_110m.url, driver="TopoJSON")

    # defintion for interactive brush
    brush = alt.selection_interval(
        encodings=["longitude"],
        empty=False,
        value={"longitude": [-50, -110]}
    )

    # world disk
    sphere = alt.Chart(alt.sphere()).mark_geoshape(
        fill="transparent", stroke="lightgray", strokeWidth=1
    )

    # countries as shapes
    world = alt.Chart(gdf_world).mark_geoshape(
        fill="lightgray", stroke="white", strokeWidth=0.1
    )

    # earthquakes as dots on map
    quakes = alt.Chart(gdf_quakies).transform_calculate(
        lon="datum.geometry.coordinates[0]",
        lat="datum.geometry.coordinates[1]",
    ).mark_circle(opacity=0.35, tooltip=True).encode(
        longitude="lon:Q",
        latitude="lat:Q",
        color=alt.when(brush).then(alt.value("goldenrod")).otherwise(alt.value("steelblue")),
        size=alt.Size("mag:Q").scale(type="pow", range=[1, 1000], domain=[0, 7], exponent=4),
    ).add_params(brush)

    # combine layers for the map
    left_map = alt.layer(sphere, world, quakes).project(type="mercator")

    # histogram of binned earthquakes
    bars = alt.Chart(gdf_quakies).mark_bar().encode(
        x=alt.X("mag:Q").bin(extent=[0,7]),
        y="count(mag):Q",
        color=alt.value("steelblue")
    )

    # filtered earthquakes
    bars_overlay = bars.encode(color=alt.value("goldenrod")).transform_filter(brush)

    # combine layers for histogram
    right_bars = alt.layer(bars, bars_overlay)

    # vertical concatenate map and bars
    final_chart = left_map | right_bars

    final_chart.save("./src/pipeline_testing/test_chart.json")
    final_chart.save("./src/pipeline_testing/test_chart.html")


