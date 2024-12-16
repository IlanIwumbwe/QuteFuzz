from typing import Tuple
from pytket.circuit import OpType, Unitary3qBox, Unitary1qBox, Unitary2qBox, Circuit, CircBox
from pytket.passes import *
from typing import List
import numpy as np
import sys
import traceback

"""
	UTILS
"""

def test_circuit_on_passes(main_circ : Circuit, test_pass : str) -> None:
	'''
	Receives: 
	- `main_circ`: internally makes a copy of it since passes act in place
	'''
	verbose = read_circ_args()

	try:
		# circuit with no passes
		no_pass_statevector = main_circ.get_statevector()
		
		# Put it through the pass specified, modifying it in-place
		all_passes[test_pass].apply(main_circ)

		# circuit after pass
		pass_statevector = main_circ.get_statevector()
		
		if np.round(abs(np.vdot(no_pass_statevector, pass_statevector)), 6)==1:
			print("Statevectors are the same\n")
		else:
			print ("Statevectors not the same")
			if (verbose): print("Dot product: ", np.round(abs(np.vdot(no_pass_statevector, pass_statevector)), 6))

	except Exception:
		print("Exception :", traceback.format_exc())

def read_circ_args() -> Tuple[bool, bool]:
	"""
		Read args passed before running the circuit
	"""
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

#Need to apply NormaliseTK2 before DecomposeTK2
def decomposeTK2() -> BasePass:
	def transform(circuit : Circuit) -> Circuit:
		NormaliseTK2().apply(circuit)
		DecomposeTK2(allow_swaps=False).apply(circuit)
		return circuit
	
	return CustomPass(transform)

all_passes = { "AutoRebase":AutoRebase({OpType.TK1, OpType.TK2}), "AutoSquash":AutoSquash({OpType.TK1}), "CliffordPushThroughMeasures":CliffordPushThroughMeasures(),
			  "CliffordResynthesis":CliffordResynthesis(), "CnXPairwiseDecomposition":CnXPairwiseDecomposition(),
			  "CommuteThroughMultis":CommuteThroughMultis(), "CliffordSimp":CliffordSimp(), "ComposePhasePolyBoxes":ComposePhasePolyBoxes(),
			  "ContextSimp":ContextSimp(), "DecomposeArbitrarilyControlledGates":DecomposeArbitrarilyControlledGates(),
			  "DecomposeMultiQubitsCX":DecomposeMultiQubitsCX(), "DecomposeSingleQubitsTK1":DecomposeSingleQubitsTK1(),
			  "DecomposeTK2":decomposeTK2(), "EulerAngleReduction":EulerAngleReduction(OpType.Rx, OpType.Ry), 
			  "FullPeepholeOptimise":FullPeepholeOptimise(), "GlobalisePhasedX":GlobalisePhasedX(), "KAKDecomposition":KAKDecomposition(),
			  "NormaliseTK2":NormaliseTK2(), "OptimisePhaseGadgets":OptimisePhaseGadgets(), "PauliExponentials":PauliExponentials(),
			  "PauliSimp":PauliSimp(), "RemoveRedundancies":RemoveRedundancies(), "SquashRzPhasedX":SquashRzPhasedX(), "SquashTK1":SquashTK1(), "SynthesiseTket":SynthesiseTket(),
			  "SynthesiseTK":SynthesiseTK(), "ThreeQubitSquash":ThreeQubitSquash(), "ZXGraphlikeOptimisation":ZXGraphlikeOptimisation(),
			  "ZZPhaseToRz":ZZPhaseToRz(), "RoundAngles":RoundAngles(0)
}
