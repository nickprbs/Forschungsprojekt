# Forschungsprojekt
Codebase for the Bachelor Research Project Winter Term 24/25


## Introduction

This project requires the use of a controller (e.g., Xbox One controller) to track inputs and visualize data using Python. Below is a step-by-step guide to set up the environment and install the required dependencies.

## Setup Guide

Follow these steps to get the project up and running:

### 1. Clone the Repository

First, clone the repository to your local machine using Git. Open a terminal and run the following command:

```bash
git clone https://github.com/nickprbs/Forschungsprojekt.git
cd Forschungsprojekt
```
### 2. Create and Set Up a Virtual Environment

A virtual environment helps you manage dependencies without interfering with other projects on your machine. The following steps will guide you through creating and activating the virtual environment.

#### On Mac/Linux:
Make Sure that the file can be executed: 
```bash
chmod +x setup.sh
```
Run the setup script in your terminal:
```bash
./setup.sh
```

#### On Windows:
Run the setup script in your console:
```bash
setup.bat
```

**Note: if you can't execute the setup script you may need to give it permission to execute**
You can do this by running the commands with admin rights
for example on mac run
```bash
sudo ./setup.sh
```
This will ask you for your password. 

On Windows you could run the terminal as an administrator.
---

If you don't want to use the setup scripts, run the following commands:


#### On Mac/Linux:
Create the virtual environment:
```bash
python3 -m venv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```
---
#### On Windows:
Create the virtual environment:
```bash
python -m venv venv
```
Activate the virtual environment: 
```bash
.\venv\Scripts\activate
```
--
After you created and activated the virtual environment, run: 
```bash
pip install -r requirements.txt
```

**Make sure that your IDE uses this virtual environment to run the code!**

## 3. Running the project
Simply head to the `src` folder and run
```bash
cd src
python simple_controller_input.py
```

## 4. Deactivating the Virtual Environment (Optional)
You can always deactivate the virtual environment by running:
```bash
deactivate
```

