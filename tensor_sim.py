"""
Quantum Circuit Simulation and Visualization Module.

This module provides tools to generate quantum circuits as tensor networks
and compare different contraction path optimization strategies.
"""

import quimb.tensor as qtn
import cotengra as ctg

def build_tensor_network(num_qubits: int, depth: int):
    
    """
    Builds a highly entangled quantum circuit and extracts its Tensor Network.

    Args:
        num_qubits (int): The number of qubits in the circuit.
        depth (int): The number of alternating CNOT layers.

    Returns:
        qtn.TensorNetwork: The mathematical tensor network representing the circuit.
    """
    
    circ = qtn.Circuit(num_qubits)

    # Add a layer of Hadamard gates
    for i in range(num_qubits):
        circ.apply_gate('H', i)

    # Add alternating layers of CNOT gates for entanglement
    for layer in range(depth):
        for i in range(num_qubits - 1):
            circ.apply_gate('CNOT', i, i+1)

    return circ.psi

def compare_contraction_paths(tn):
    
    """
    Compares the computational cost (FLOPs) of a standard Greedy optimizer 
    versus a Hyper-Optimizer for a given Tensor Network.

    Args:
        tn (qtn.TensorNetwork): The tensor network to be contracted.

    Returns:
        float: The speedup factor achieved by the hyper-optimizer.
    """
    
    # 1. Greedy Optimizer
    opt_greedy = ctg.GreedyOptimizer()
    info_greedy = tn.contract(all, get='path-info', optimize=opt_greedy)
    flops_greedy = info_greedy.opt_cost

    # 2. Hyper Optimizer (allows a few seconds to find a better path)
    opt_hyper = ctg.HyperOptimizer(max_time=5)
    info_hyper = tn.contract(all, get='path-info', optimize=opt_hyper)
    flops_hyper = info_hyper.opt_cost

    speedup = flops_greedy / flops_hyper
    
    print(f"Standard Greedy FLOPs: {flops_greedy:.2e}")
    print(f"Hyper-Optimized FLOPs: {flops_hyper:.2e}")
    print(f"Speedup Factor: ~{int(speedup)}X")
    
    return speedup