# ALOHA Protocol Simulation

## 1. Project Overview

The ALOHA Protocol Simulation is a Python-based project that demonstrates and compares two random-access communication protocols: Pure ALOHA and Slotted ALOHA.

The project simulates data transmission, identifies collisions, calculates successful transmissions and evaluates throughput under different traffic loads. An interactive Streamlit dashboard allows users to run simulations and visualize the results.

## 2. Abstract

ALOHA is a random-access protocol used in communication networks to manage how multiple devices share a common communication channel.

This project implements Pure ALOHA and Slotted ALOHA using Python. It analyzes how offered traffic load affects successful transmission, collisions and throughput. The project also provides an interactive dashboard with graphs, comparison tables and downloadable CSV reports.

The simulation helps users understand the performance differences between the two protocols under different network traffic conditions.

## 3. Objectives

- Implement Pure ALOHA and Slotted ALOHA using Python.
- Simulate successful and collided transmissions.
- Calculate throughput under different traffic loads.
- Compare the performance of both protocols.
- Display simulation results through interactive graphs and tables.
- Generate downloadable CSV reports.

## 4. Technologies Used

- Programming Language: Python
- Dashboard Framework: Streamlit
- Data Visualization: Matplotlib
- Data Processing: Pandas
- Development Environment: Visual Studio Code

## 5. Modules

### Pure ALOHA
Allows frames to be transmitted at any time. Collisions occur when transmission periods overlap.

### Slotted ALOHA
Divides time into slots. Devices can transmit only at the beginning of a slot.

### Comparison Module
Compares simulation results and generates throughput graphs and CSV reports.

### Dashboard Module
Provides an interactive interface for selecting traffic load, running simulations and viewing results.

## 6. Working Methodology

1. The user selects the offered traffic load and simulation size.
2. The system runs the Pure ALOHA simulation.
3. The system runs the Slotted ALOHA simulation.
4. Transmission successes and collisions are calculated.
5. Throughput is calculated for both protocols.
6. Results are displayed through graphs and comparison tables.
7. Users can download the generated reports.

## 7. Mathematical Formulas

Pure ALOHA:

S = G × e^(-2G)

Slotted ALOHA:

S = G × e^(-G)

Where:
- S = Throughput
- G = Offered traffic load
- e = Euler's mathematical constant

## 8. Main Features

- Interactive simulation dashboard
- Pure and Slotted ALOHA simulation
- Collision and throughput analysis
- Multiple traffic load analysis
- Graphical comparison
- CSV report downloads

## 9. How to Run the Project

1. Open the project folder in Visual Studio Code.
2. Activate the virtual environment.
3. Install the required packages if needed:

   pip install streamlit matplotlib pandas numpy

4. Run the dashboard:

   streamlit run app.py

