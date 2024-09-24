from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import XGate
from qiskit.transpiler.passes import *
from qiskit.transpiler import PassManager, generate_preset_pass_manager
from qiskit.quantum_info import Statevector
from numpy import vdot
from typing import Dict, Tuple, List
from collections import Counter
from itertools import zip_longest
from scipy.stats import ks_2samp
from qiskit.visualization import plot_histogram
import sys, random, pathlib, numpy as np

# List of all optimisation compiler passes
opt_passes = {  "Optimize1qGates": Optimize1qGates(), "Optimize1qGatesDecomposition":Optimize1qGatesDecomposition(),
                "Collect1qRuns": Collect1qRuns(), "Collect2qBlocks": Collect2qBlocks(),
                "CollectMultiQBlocks":CollectMultiQBlocks(),"CollectLinearFunctions":CollectLinearFunctions(),
                "CollectCliffords":CollectCliffords(),"ConsolidateBlocks":ConsolidateBlocks(),
                "CXCancellation":CXCancellation(),"InverseCancellation":InverseCancellation([XGate()]),
                "CommutationAnalysis":CommutationAnalysis(),"CommutativeCancellation":CommutativeCancellation(),
                "CommutativeInverseCancellation":CommutativeInverseCancellation(),
                "Optimize1qGatesSimpleCommutation":Optimize1qGatesSimpleCommutation(),
                "RemoveDiagonalGatesBeforeMeasure":RemoveDiagonalGatesBeforeMeasure(),
                "RemoveResetInZeroState":RemoveResetInZeroState(),"RemoveFinalReset":RemoveFinalReset(),
                "HoareOptimizer":HoareOptimizer(),"TemplateOptimization":TemplateOptimization(),
                "ResetAfterMeasureSimplification":ResetAfterMeasureSimplification(), #"EchoRZXWeylDecomposition":EchoRZXWeylDecomposition(),
                "OptimizeCliffords":OptimizeCliffords(),"ElidePermutations":ElidePermutations(),
                "NormalizeRXAngle":NormalizeRXAngle(),"OptimizeAnnotated":OptimizeAnnotated()
            }

'''
Helper functions
'''
def generate_custom_mapping(num_qubits : int) -> List[List]:
    # This is an array holding the generated map
    map = []

    # First ensure all qubits are at least connected to 1 other qubit
    free_qubits = list(range(1, num_qubits))
    paired_qubits = [0]
    while(len(free_qubits)):   #While there are still qubits to be added, continue
        q0 = free_qubits.pop(random.randrange(0, len(free_qubits)))
        q1 = paired_qubits[random.randrange(0, len(paired_qubits))]
        paired_qubits.append(q0)    # Re-insert the popped qubit into list of paired qubits
        map.append([q0, q1])

    # The generate a random amount of extra connections between qubits (can repeat)
    for _ in range(random.randint(0, 10)):
        q0 = paired_qubits[random.randrange(0, len(paired_qubits))]
        while (q1 == q0):
            q1 = paired_qubits[random.randrange(0, len(paired_qubits))]
        map.append([q0, q1])
    
    return map

def read_circ_args() -> Tuple[bool, bool]:
	args : List[str] = sys.argv
	verbose : bool = False
	plot : bool = False

	if(len(args) == 3):
		verbose, plot = args[1] == "-v", args[2] == "-p"

	elif(len(args) == 2):
		verbose, plot = args[1] == "-v", args[1] == "-p"

	elif(len(args) != 1):
		print("Usage: <FILE>.py [-v] [-p]")

	return verbose, plot

def simulate_circuit(qc : QuantumCircuit):
    state = Statevector.from_int(0, 2**qc.num_qubits)

    state = state.evolve(qc)

    return state

def preprocess_counts(counts :  Counter[Tuple[str, ...], int]) -> Counter[Tuple[int, ...], int]:
	'''
		Convert into the correct output type 
	'''
	out : Counter[Tuple[int, ...], int] = {}

	for k in counts.keys():
		out[tuple([int(i) for i in k.replace(' ','')])] = counts[k]

	return out

def ks_test(counts1 : Counter[Tuple[int, ...], int], counts2 : Counter[Tuple[int, ...], int], total_shots : int) -> float:
	'''
	Carries out K-S test on two frequency lists
	'''
	sample1, sample2 = [], []

	for p1, p2 in zip_longest(counts1.items(), counts2.items(), fillvalue=None):
		num1, num2 = 0, 0

		if(p1):
			for i in range(len(p1[0])): num1 += (p1[0][i] * (2**(len(p1[0]) - i)))
			sample1 += p1[1] * [num1]
		
		if(p2):
			for i in range(len(p2[0])): num2 += (p2[0][i] * (2**(len(p2[0]) - i)))
			sample2 += p2[1] * [num2]

	assert (len(sample1) == total_shots) and (len(sample2) == total_shots), "Sample size does not match number of shots"

	ks_stat, p_value = ks_2samp(sorted(sample1), sorted(sample2))


	'''
		Counter({(1, 1, 0, 0, 0): 25034, (1, 0, 0, 0, 0): 24966})
		Counter({(1,0,0,0,0,):24500, (1,1,0,0,0,):25500})
	'''

	return p_value  

'''
Called functions
'''
def compare_statevectors(qc : QuantumCircuit, pass_to_do : str):
    # AllOpt stands for default transpiler passes
    if pass_to_do == "AllOpt":
        # Need to set the seed for consistent transpiler pass results across optimisation levels
        options = {'layout_method': 'trivial', 'seed_transpiler': 1235, 'routing_method': 'stochastic', 'translation_method': 'translator'}
        sv0 = simulate_circuit(qc)
        # Code for checking different levels of optimization levels and if they are the same
        for i in range(4):
            pass_manager = generate_preset_pass_manager(optimization_level=i, **options)
            transpiled_circuit = pass_manager.run(qc)
            sv = simulate_circuit(transpiled_circuit)

            if(np.isclose(1.0 , abs(vdot(sv0, sv)), rtol=0, atol=1e-8)):
                print("Level ", i, " passed")
            else:
                print("Failed level ", i, ". Dot product is: " , abs(vdot(sv0, sv)), "\n")

    else:
        # Code for inidividual compiler pass testing
        print("Testing", pass_to_do)
        
        pass_to_do = PassManager(opt_passes[pass_to_do])
        pass_circ = pass_to_do.run(qc)

        sv0 = simulate_circuit(qc)
        sv1 = simulate_circuit(pass_circ)

        # Compare the circuit statevector before and after the pass
        if(np.isclose(1.0, abs(vdot(sv0, sv1)), rtol=0, atol=1e-8)):
            print("Passed test!\n")
        else:
            print("Failed test!")
            print("dot product is: ", abs(vdot(sv0, sv1)), "\n") 

def run_on_simulator(qc : QuantumCircuit, circuit_number : int):
    # Lazy importing to speed up other circuits
    from qiskit_aer import AerSimulator
    s = AerSimulator()

    qc1 = transpile(qc, s, optimization_level=0)
    c1 = s.run(qc1, shots=1024).result().get_counts()

    c1 = preprocess_counts(c1)

    verbose, plot = read_circ_args()
	
    if(plot): 
        pathlib.Path("quantum_cirucits/plots").mkdir(exist_ok=True)
        plot_histogram(c1, figsize=[9,5], filename="quantum_circuits/plots/circuit"+str(circuit_number)+".png")
    
    ks_vals = []

    for i in range(1, 4):
        qcT = transpile(qc, s, optimization_level=i)
        c = s.run(qcT, shots=1024).result().get_counts()
        c = preprocess_counts(c)

        ks_vals.append(ks_test(c1, c, 1024))
    
    print(ks_vals, "\n")

def run_routing_simulation(qc : QuantumCircuit, circuit_number : int):
    # Lazy importing of Backend
    from qiskit.providers.fake_provider import GenericBackendV2
    
    s_unrestricted = GenericBackendV2(num_qubits=qc.num_qubits, seed=1234, noise_info=False)

    # Level 0 to have minimum optimisation while achieving routing pass
    new_circ_lv0 = transpile(qc, backend=s_unrestricted, optimization_level=0, target=s_unrestricted.target)
    counts_unrestricted = preprocess_counts(s_unrestricted.run(new_circ_lv0, shots=1024).result().get_counts())

    verbose, plot = read_circ_args()
    if(plot): 
        pathlib.Path("quantum_cirucits/plots").mkdir(exist_ok=True)
        plot_histogram(counts_unrestricted, figsize=[9,5], filename="quantum_circuits/plots/circuit"+str(circuit_number)+".png")

    map = generate_custom_mapping(qc.num_qubits)
    s_restricted = GenericBackendV2(num_qubits=qc.num_qubits, seed=1234, coupling_map=map, noise_info=False)
    print("Testing custom routing map: ", map)

    ks_vals = []
    for i in range(0, 4):
        qcT = transpile(qc, s_restricted, optimization_level=i)
        c = s_restricted.run(qcT, shots=1024).result().get_counts()
        c = preprocess_counts(c)
        
        ks_vals.append(ks_test(counts_unrestricted, c, 1024))
        
        # Uncomment for debugging
        # print(dict(sorted(c.items())))

        if(plot): 
            pathlib.Path("quantum_cirucits/plots").mkdir(exist_ok=True)
            plot_histogram(c, figsize=[9,5], filename="quantum_circuits/plots/circuit"+str(circuit_number)+"_"+str(i)+".png")

    # Simply prints the ksvals for manual validation
    print(ks_vals, "\n")
    