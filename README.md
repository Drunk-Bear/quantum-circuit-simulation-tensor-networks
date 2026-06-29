# Quantum Circuit Simulation and Visualization

## Overview
This repository contains the practical implementation for the "Advanced Topics of Quantum Computing" (AQC) Seminar at the Technical University of Munich (TUM). 

The project explores the classical simulation of Random Quantum Circuits (RQCs) by mapping them to **Tensor Networks**. Based on the paper *"Hyper-optimized tensor network contraction"* (Gray & Kourtis, 2021), this implementation demonstrates the massive computational speedup achieved by using hyper-optimized contraction paths instead of standard greedy algorithms.

## Recent Upgrades & Numerical Experiments
Following the seminar presentation feedback, this repository has been significantly upgraded to include comprehensive numerical experiments and "own work" demonstrations:
1. **Real-world Execution Benchmarking:** Added functionality to measure actual tensor contraction time in seconds, distinguishing between path optimization and physical matrix multiplication.
2. **2D Scaling Analysis:** Implemented a heatmap analysis to evaluate the speedup factor as both circuit depth and the number of qubits increase.
3. **Manual Tensor Contraction:** Included a pure linear algebra demonstration (`numpy.einsum`) to construct a Bell State from scratch, proving the underlying mathematical mechanics without relying on high-level libraries.

## Repository Structure
To maintain readability and a clean architecture, the project is structured as follows:

* `tensor_sim.py`: The core Python module. It contains the logic to build highly entangled quantum circuits, extract their underlying mathematical tensor networks, calculate theoretical contraction costs (FLOPs), and perform manual tensor math.
* `main.ipynb`: A Jupyter Notebook that serves as the entry point. It imports the module, generates the 3D visualization, and runs the numerical experiments (including real-time benchmarking and 2D scaling heatmaps).
* `README.md`: This documentation file.
* `CITATION.cff` & `LICENSE`: Information for citing this work and the open-source MIT License terms.

## Requirements and Installation
The project requires Python 3. To run the simulation, visualize the networks, and plot the benchmarks, you need to install the following core dependencies:

```bash
pip install quimb cotengra networkx jupyterlab matplotlib seaborn kahypar numpy