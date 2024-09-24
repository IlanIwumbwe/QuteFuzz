#include "../headers/gate.h"

std::vector<Circuit_Restrictions> pytket_opt_passes = {Circuit_Restrictions{"AutoRebase", primitive | tk1 | tk2 | two_qubit_gate | clifford | rotation | phased, no_circbox | no_paulibox | no_mult}, 
	Circuit_Restrictions{"CliffordResynthesis", two_qubit_gate | clifford,  no_circbox | no_paulibox}, 
	Circuit_Restrictions{"CliffordPushThroughMeasures", clifford},
	Circuit_Restrictions{"CnXPairwiseDecomposition", two_qubit_gate | primitive}, 
	Circuit_Restrictions{"CommuteThroughMultis", two_qubit_gate | primitive | clifford | rotation},
	Circuit_Restrictions{"ComposePhasePolyBoxes", primitive | tk1 | tk2 | two_qubit_gate | clifford | rotation, no_circbox | no_mult | no_paulibox | no_named_qubits},
	Circuit_Restrictions{"ContextSimp", primitive | tk1 | tk2 | two_qubit_gate | clifford | rotation},
	Circuit_Restrictions{"DecomposeArbitrarilyControlledGates", primitive | two_qubit_gate, no_mult | no_circbox | no_paulibox},
	Circuit_Restrictions{"DecomposeSingleQubitsTK1", primitive | tk1 | tk2 | clifford | rotation},
	// Circuit_Restrictions{"DecomposeTK2", {basis, tk_gates}},  // need to apply NormaliseTK2 to normalise parameters
	Circuit_Restrictions{"EulerAngleReduction", primitive | rotation},
	Circuit_Restrictions{"FullPeepholeOptimise", primitive | rotation, no_paulibox | no_circbox | no_mult},
	// Circuit_Restrictions{"GlobalisePhasedX", primitive | phased},
	Circuit_Restrictions{"KAKDecomposition", two_qubit_gate, no_circbox | no_paulibox | no_mult},
	Circuit_Restrictions{"OptimisePhaseGadgets", phased,  no_circbox | no_paulibox},
	Circuit_Restrictions{"PauliExponentials", two_qubit_gate | rotation | phased, no_circbox | no_mult},
	Circuit_Restrictions{"PauliSimp", two_qubit_gate | rotation | phased, no_circbox | no_mult},
	Circuit_Restrictions{"RemoveRedundancies", primitive | tk1 | tk2 | two_qubit_gate | clifford | rotation | phased},
	Circuit_Restrictions{"SquashRzPhasedX", primitive | clifford | rotation},
	Circuit_Restrictions{"SquashTK1", primitive | clifford | rotation},
	Circuit_Restrictions{"SynthesiseTK", primitive | tk1 | tk2 | two_qubit_gate | clifford | rotation | phased, no_circbox | no_paulibox | no_mult},
	Circuit_Restrictions{"SynthesiseTket", primitive | tk1 | tk2 | two_qubit_gate | clifford | rotation | phased, no_circbox | no_paulibox | no_mult},
	Circuit_Restrictions{"ThreeQubitSquash", primitive | cx | rotation, no_paulibox | no_circbox | no_mult},
	Circuit_Restrictions{"ZXGraphlikeOptimisation", cz | z | cx | x | noop | swap | rx | rz | h, no_paulibox | no_circbox | no_mult | no_bits | no_named_qubits},
};

/// @brief Empty strings imply that the gate doesn't exist for that front end. This gate type will never be used by that front-end anyway
std::vector<gate_mapping> gate_names = {
    {x, {"X", "x", "X"}},
    {y, {"Y", "y", "Y"}},
    {z, {"Z", "z", "Z"}},
    {v, {"V", "v", "V"}},
    {u3, {"U3", "u3", "U3"}},
    {u2, {"U2", "u2", "U2"}},
    {u1, {"U1", "u1", "U1"}},
    {swap, {"SWAP", "swap", "SWAP"}},
    {tk1, {"TK1", "", ""}},   
    {tk2, {"TK2", "", ""}},
    {cx, {"CX", "cx", "CNOT"}},
    {cy, {"CY", "cy", ""}},
    {cz, {"CZ", "cz", "CZ"}},
    {s, {"S", "s", "S"}},
    {cnx, {"CnX", "cnx", ""}},
    {cny, {"CnY", "cny", ""}},
    {cnz, {"CnZ", "cnz", ""}},
    {cnrx, {"CnRx", "cnrx", ""}},
    {cnry, {"CnRy", "cnry", ""}},
    {cnrz, {"CnRz", "cnrz", ""}},
    {crx, {"CRx", "crx", ""}},
    {cry, {"CRy", "cry", ""}},
    {crz, {"CRz", "crz", ""}},
    {noop, {"noop", "noop", ""}},
    {xxphase, {"XXPhase", "yyphase", ""}},
    {yyphase, {"YYPhase", "yyphase", ""}},
    {zzphase, {"ZZPhase", "zzphase", ""}},
    {h, {"H", "h", ""}},
    {rx, {"Rx", "rx", "rx"}},
    {ry, {"Ry", "ry", "ry"}},
    {rz, {"Rz", "rz", "ry"}},
    {sx, {"", "sx", ""}},
    {multiplexor, {"multiplexor", "multiplexor"}},
    {paulibox, {"pauli_box", "pauli_box"}},
    {u, {"", "u", ""}},
    {t, {"","","T"}},
    {cswap, {"","","CSWAP"}},
    {phasedxz, {"","","PhasedXZGate"}},
    {phasedxpow, {"","","PhasedXPowGate"}}
};

std::string get_gate_name(gate_type t){
    for (gate_mapping& m : gate_names){
        if(m.t == t){
            return m.names[f];
        }
    }

    std::cerr << "Name for gate of type " << t << " is not supported " << std::endl;
    exit(-1);
}