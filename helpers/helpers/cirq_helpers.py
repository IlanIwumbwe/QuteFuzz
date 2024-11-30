import numpy as np
from cirq import *
from sympy import true
from typing import Dict, Tuple, List
from collections import Counter
from itertools import zip_longest
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt
import sys, pathlib
from cirq.transformers import *

quantum_circuits_path = pathlib.Path("quantum_circuits")
plots_path = quantum_circuits_path / "plots"

# All passes are not done in-place
all_passes = {"stratified_circuit": stratified_circuit,
			  "merge_single_qubit_gates_to_phased_x_and_z": merge_single_qubit_gates_to_phased_x_and_z,
			  "merge_single_qubit_gates_to_phxz": merge_single_qubit_gates_to_phxz,
			  "merge_single_qubit_moments_to_phxz": merge_single_qubit_moments_to_phxz,
			  "merge_k_qubit_unitaries": merge_k_qubit_unitaries,
			  "expand_composite": expand_composite,
			  "eject_z": eject_z, "eject_phased_paulis": eject_phased_paulis,
			  "add_dynamical_decoupling": add_dynamical_decoupling,
			  "drop_negligible_operations": drop_negligible_operations,
			  "drop_empty_moments": drop_empty_moments,
			  "align_left": align_left, "align_right": align_right,
			  }

target_gatesets = {"cz(allow_partial=True)" : CZTargetGateset(allow_partial_czs=true), "cz(allow_partial=False)" : CZTargetGateset(), "sqrtiswap" : SqrtIswapTargetGateset()}

def ks_test(counts1 : Counter[int, int], counts2 : Counter[int, int], total_shots : int) -> float:
	'''
	Carries out K-S test on two frequency lists
	'''
	sample1, sample2 = [], []

	for p1, p2 in zip_longest(counts1.items(), counts2.items(), fillvalue=None):

		if(p1):
			sample1 += p1[1] * [p1[0]]
		
		if(p2):
			sample2 += p2[1] * [p2[0]]

	assert (len(sample1) == total_shots) and (len(sample2) == total_shots), "Sample size does not match number of shots"

	ks_stat, p_value = ks_2samp(sorted(sample1), sorted(sample2))

	return p_value

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

def plot_cirq_dist(c_orig, c_new, circ_num : int) -> None:
	"""
		Plot distributions of results for original vs optimised circuit
	"""
	
	plots_path.mkdir(exist_ok=True)

	filename_orig = plots_path / ("Circ"+str(circ_num)+"_Original")
	filename_new = plots_path / ("Circ"+str(circ_num)+"_New")

	plot_state_histogram(c_orig, plt.subplot())
	plt.savefig(filename_orig)
	plt.close()
	plot_state_histogram(c_new, plt.subplot())
	plt.savefig(filename_new)
	plt.close()

def compare_circuits(circ : Circuit, gs : str, circ_num : int):
	simulator = Simulator()
	context = TransformerContext(tags_to_ignore=("nocompile",), deep=True, logger=TransformerLogger())
	target_gateset = target_gatesets[gs]
	shots = 1024

	verbose, plot = read_circ_args()

	circ_new = optimize_for_target_gateset(circuit=circ, context=context, gateset=target_gateset)
	c_orig = simulator.run(circ, repetitions=shots).histogram(key="results")
	c_new = simulator.run(circ_new, repetitions=shots).histogram(key='results')

	print(ks_test(c_orig, c_new, shots), "\n")

	if(plot): 
		plot_cirq_dist(c_orig, c_new, circ_num)

def individual_pass(circ : Circuit, circ_num : int, pass_to_do : str):
	simulator = Simulator()
	shots = 1024

	verbose, plot = read_circ_args()

	# Takes the modified copy of circ
	if pass_to_do == "merge_k_qubit_unitaries":
		circ_new = all_passes[pass_to_do](circ, k=np.random.randint(1, 5))
	else :
		circ_new = all_passes[pass_to_do](circ)
	c_orig = simulator.run(circ, repetitions=shots).histogram(key="results")
	c_new = simulator.run(circ_new, repetitions=shots).histogram(key='results')

	print(ks_test(c_orig, c_new, shots), "\n")

	if(plot): 
		plot_cirq_dist(c_orig, c_new, circ_num)