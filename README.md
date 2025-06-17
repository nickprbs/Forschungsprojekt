# Gamepad Controls for Visualizations
This repository contains the code artifacts that have been produced throughout the duration of the project, including [several prototypes](/src/prototypes/) and [visualizations](/src/visualizations/). 

![](/images/teaser.png) 

## File Overview

The ```src``` directory contains the following project files: 

  - ```datasets```: Folder where all converted CSV datasets are stored
    - ```yearly_avg_2015_to_2099_downsampled.csv```: Data used to build the visualizations
  - ```prototypes```: Folder where all different prototypes are stored
    - ```final_dynamic_prototype```: Fully interactive mockups of the scatterplot *building mode*  and bar chart *interval mode*
    - ```final_static_prototype```: Interactive prototype that contains tutorial paths which the user can explore 
    - ```final_prototype```: Combination of the static and dynamic prototypes 
    - ```first_prototype```: Initial prototype based on sketches 
  - ```visualizations```: Stores all files related to building and rendering the visualizations
    - ```outputs```: Miscellaneous files produced and used by the visualization builder
    - ```visualization_builder.ipynb```: Jupyter Notebook that contains all the different chart specifications based on the dataset. 
  - ```nc_to_csv_converter```: Converts .nc to csv files and saves the result in the datasets folder
