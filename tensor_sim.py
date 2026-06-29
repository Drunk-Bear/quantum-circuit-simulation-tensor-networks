"""
Quantum Circuit Simulation and Visualization Module.

This module provides the core computational backend for the AQC Seminar.
It includes functionalities to:
1. Build highly entangled Random Quantum Circuits (RQCs) mapped as Tensor Networks.
2. Evaluate theoretical computational costs (FLOPs) using graph partitioning heuristics.
3. Perform actual tensor contractions to measure real-world execution time.
4. Demonstrate manual tensor contraction using pure linear algebra (numpy) as 'own work'.
"""

import quimb.tensor as qtn
import cotengra as ctg
import time
import numpy as np

def build_tensor_network(num_qubits: int, depth: int):
    """
    Constructs a highly entangled quantum circuit and extracts its Tensor Network representation.

    The circuit is initialized with a layer of Hadamard gates to create an equal 
    superposition, followed by alternating layers of CNOT gates. This structure 
    rapidly increases the entanglement entropy (bond dimension), effectively simulating 
    the complexity of a Random Quantum Circuit (RQC) that challenges classical simulators.

    Args:
        num_qubits (int): The width of the circuit (number of qubits).
        depth (int): The number of alternating CNOT layers applied for entanglement.

    Returns:
        qtn.TensorNetwork: The purely mathematical graph representing the quantum state, 
                           where nodes are gates and edges are contraction indices.
    """
    circ = qtn.Circuit(num_qubits)

    # Layer 1: Hadamard gates for superposition
    for i in range(num_qubits):
        circ.apply_gate('H', i)

    # Layer 2: CNOT gates to generate entanglement
    for layer in range(depth):
        for i in range(num_qubits - 1):
            circ.apply_gate('CNOT', i, i+1)

    return circ.psi

def compare_contraction_paths(tn):
    """
    Evaluates and prints the theoretical speedup between a standard Greedy optimizer 
    and a Hyper-Optimizer (using graph partitioning techniques like kahypar).

    This function specifically requests 'path-info' without performing the actual 
    matrix multiplication, allowing us to benchmark massive circuits without 
    running out of memory.

    Args:
        tn (qtn.TensorNetwork): The tensor network object to be analyzed.

    Returns:
        float: The calculated speedup factor (Greedy FLOPs / Hyper-Optimized FLOPs).
    """
    # 1. Standard Greedy Approach
    opt_greedy = ctg.GreedyOptimizer()
    info_greedy = tn.contract(all, get='path-info', optimize=opt_greedy)
    flops_greedy = info_greedy.opt_cost

    # 2. Hyper-Optimized Approach (Min-Cut / Graph Partitioning)
    opt_hyper = ctg.HyperOptimizer(max_time=5)
    info_hyper = tn.contract(all, get='path-info', optimize=opt_hyper)
    flops_hyper = info_hyper.opt_cost

    speedup = flops_greedy / flops_hyper
    
    print(f"Standard Greedy FLOPs: {flops_greedy:.2e}")
    print(f"Hyper-Optimized FLOPs: {flops_hyper:.2e}")
    print(f"Speedup Factor: ~{int(speedup)}X")
    
    return speedup

def get_raw_flops(tn):
    """
    Silently calculates the exact computational cost (FLOPs) for plotting purposes.
    
    Unlike 'compare_contraction_paths', this function returns the raw values directly 
    without printing to the console, making it ideal for running loops in 2D scaling 
    experiments (e.g., generating Heatmaps).

    Args:
        tn (qtn.TensorNetwork): The tensor network to be analyzed.

    Returns:
        tuple: (Greedy FLOPs cost, Hyper-Optimized FLOPs cost)
    """
    opt_greedy = ctg.GreedyOptimizer()
    info_greedy = tn.contract(all, get='path-info', optimize=opt_greedy)
    
    opt_hyper = ctg.HyperOptimizer(max_time=2) 
    info_hyper = tn.contract(all, get='path-info', optimize=opt_hyper)
    
    return info_greedy.opt_cost, info_hyper.opt_cost

def execute_and_time_contraction(tn):
    """
    Performs the physical tensor contraction (actual matrix multiplication) 
    and measures the real execution time in seconds.

    This function proves the real-world impact of the optimized contraction path.
    Warning: Running this on highly entangled circuits (e.g., >30 qubits) will 
    cause an exponential memory blow-up.

    Args:
        tn (qtn.TensorNetwork): The tensor network to be physically contracted.

    Returns:
        tuple: (Execution time of Greedy in seconds, Execution time of Hyper-Optimized in seconds)
    """
    opt_greedy = ctg.GreedyOptimizer()
    start_greedy = time.time()
    _ = tn.contract(all, optimize=opt_greedy)
    time_greedy = time.time() - start_greedy
    
    opt_hyper = ctg.HyperOptimizer(max_time=2)
    start_hyper = time.time()
    _ = tn.contract(all, optimize=opt_hyper)
    time_hyper = time.time() - start_hyper
    
    return time_greedy, time_hyper

def manual_tensor_contraction_demo():
    """
    Demonstrates the underlying linear algebra of a Tensor Network manually.
    
    Instead of relying on high-level libraries like 'quimb', this function uses 
    Einstein Summation (numpy.einsum) to contract a small 2-qubit circuit (creating 
    a Bell State) from scratch. This showcases the fundamental tensor mechanics:
    Node (Gate) * Edge (State) = New State.

    Returns:
        np.ndarray: The final statevector amplitudes after contraction.
    """
    # 1. Initialize two qubits in the basis state |0>
    q0 = np.array([1.0, 0.0])
    q1 = np.array([1.0, 0.0])
    
    # 2. Define the quantum gates as pure mathematical tensors
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    CNOT = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]]).reshape(2,2,2,2)
    
    # 3. Contract the Hadamard tensor with the first qubit tensor
    q0_H = np.einsum('ij,j->i', H, q0)
    
    # 4. Contract the CNOT tensor with both qubits to create entanglement
    bell_state = np.einsum('ijkl,k,l->ij', CNOT, q0_H, q1)
    
    # Flatten the tensor back into a 1D statevector for readability
    return bell_state.flatten()