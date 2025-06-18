# Bachelor Research Project: Gamepad Controls for Visualizations
This repository contains the code artifacts that have been produced during the project, including [several prototypes](/src/prototypes/) and [visualizations](/src/visualizations/). 

![](/images/teaser.png) 

__Examiner:__ Dr. Guido Reina

__Supervisors:__ Dr. Marina Evers, Sergej Geringer

The goal of this research project is to investigate how gamepads can be used as input devices for available visualization toolkits, to analyze and define typical user tasks with common 2D (and 3D) visualization techniques (e.g., parallel coordinates plots, scatter plot matrices, tree maps), and to implement gamepad-controls for visualizations based on this analysis, i.e., define mappings from
visualization user tasks/actions to gamepad inputs (buttons) or to different input modes. 

# Thesis Goals
- Literature Research:
- Gamepads in user interaction and gaming
- Typical information-visualizations (e.g., scatter plot, PCP)
- User tasks and actions in visualizations
- Research relevant programming libraries and frameworks
- Receive gamepad inputs
- Build small visualizations
- Implement a visualization application controlled by a gamepad:
  1. Assess visualization user tasks for visualization techniques
  2. Based on tasks, prototype and implement gamepad inputs for chosen visualization
techniques and toolkits/libraries:
    - Line and bar charts
    - Parallel Coordinates Plot (PCP)
    - Scatterplot Matrix (SPLOM)
    - 3D Visualization of the Earth
  3. Integrate individual visualization techniques into an application that supports the visual
analysis of climate data with multiple linked views and gamepad interactions
- Evaluate the implementation, e.g. with a small interview study with visualization experts
- Bonus Goal: implement local multi-user support for visualization app: two or more
users/gamepads
- Write a report about your work
- Present your work in a final presentation
- Provide a 2-minute video which shows your work and results

# Installation

### Requirements:
+ All prototypes have been developed based on the inputs of a **Sony PS5 DualSense Controller** that is connected to the device via **Bluetooth**. Other controllers and/or connection methods are not guaranteed to work. 
+ Python needs to be installed, we recommend using Python3.13 or higher

### Project Setup:
1. Clone the repository e.g. by running `git clone https://github.tik.uni-stuttgart.de/VISUSstud/PRJ-ProbstTrackUkrainskyAbualqumboz-GamepadControlsForVisualizations.git`
2. Change into the project directory `cd PRJ-ProbstTrackUkrainskyAbualqumboz-GamepadControlsForVisualizations`
3. Install the required python packages: `pip install -r requirements.txt` . We recommend using a virtual environment to avoid compatibility issues if you work with other Python projects. More information on virtual environments can be found [here](https://docs.python.org/3/library/venv.html).

### Launching Prototypes
As a first step, please make sure that your DualSense Controller is connected to your machine via Bluetooth. After that, proceed based on the selected prototype:

+ **First Prototype**: Start the prototype by executing its [`prototyp.py`](/src/prototypes/first_prototype/prototyp.py) file, e.g. by running the follwing command from the project folder: `python3 ./src/prototypes/first_prototype/prototyp.py` .
+ **Final Static Prototype**: Execute the corresponding [`prototype.py`](./src/prototypes/final_static_prototype/prototype.py) file, e.g. with: `python3 ./src/prototypes/final_static_prototype.py` from the project folder.
+ **Final Dynamic Prototype**: Contains two seperate prototypes. Simply execute the desired `.py`file.
+ **Final Prototype**: Execute the corresponding[`prototype.py`](/src/prototypes/final_prototype/prototype.py) file to start the final prototype.

### Building and Viewing Visualizations
The Specifications are stored inside the [`visualization_builder.ipynb`](/src/visualizations/visualization_builder.ipynb).You can view them simply by executing a code cell (and all the initial setup cells) inside the Jupyter Notebook. We recommend using Visual Studio Code with the according Jupyter extensions to work with the notebook. 

**Note**: Some cells inside the notebook will open charts as new tabs in your standard browser, because Jupyter is not able to render them properly.

# File Overview

The `src` directory contains the following project files: 

  - `datasets`: Folder where all converted CSV datasets are stored
    - `yearly_avg_2015_to_2099_downsampled.csv`: Data used to build the visualizations
  - `prototypes`: Folder where all different prototypes are stored
    - `final_dynamic_prototype`: Fully interactive mockups of the scatterplot *building mode*  and bar chart *interval mode*
    - `final_static_prototype`: Interactive prototype that contains tutorial paths which the user can explore 
    - `final_prototype`: Combination of the static and dynamic prototypes 
    - `first_prototype`: Initial prototype based on sketches 
  - `visualizations`: Stores all files related to building and rendering the visualizations
    - `outputs`: Miscellaneous files produced and used by the visualization builder
    - `visualization_builder.ipynb`: Jupyter Notebook that contains all the different chart specifications based on the dataset. 
  - `nc_to_csv_converter`: Converts .nc to csv files and saves the result in the datasets folder

---
