# Quantum Circuit Simulation and Visualization

## Overview
This repository contains the practical implementation for the "Advanced Topics of Quantum Computing" (AQC) Seminar at the Technical University of Munich (TUM). 

The project explores the classical simulation of Random Quantum Circuits (RQCs) by mapping them to **Tensor Networks**. Based on the paper *"Hyper-optimized tensor network contraction"* (Gray & Kourtis, 2021), this implementation demonstrates the massive computational speedup achieved by using hyper-optimized contraction paths instead of standard greedy algorithms.

## Repository Structure
To maintain readability and a clean architecture, the project is structured as follows:

* `tensor_sim.py`: The core Python module. It contains the logic to build the highly entangled quantum circuits, extract their underlying mathematical tensor networks, and compare different contraction algorithms. It includes standard docstrings.
* `main.ipynb`: A clean Jupyter Notebook that serves as the entry point. It imports the module and runs a single example case, generating the 3D visualization and the performance comparison output.
* `README.md`: This documentation file.

## Requirements and Installation
The project requires Python 3. To run the simulation and visualize the networks, you need to install the following core dependencies:

```bash
pip install quimb cotengra networkx jupyterlab