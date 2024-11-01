#include "../headers/utils.h"
#include <iostream>

frontend f = f_pytket;

// constants 
const int MIN_TOTAL_QUBITS = 4;
const int MAX_TOTAL_QUBITS = 6;
const int MIN_TOTAL_GATES = 20;
const int MAX_TOTAL_GATES = 70;
const int MAX_ADDED_CIRCBOX_QUBITS = 2;
const int MIN_CIRCBOX_GATES = 4;
const int MAX_CIRCBOX_GATES = 6;
const int MAX_CIRCBOX_CONTROL_QUBITS = 3;
const int MAX_CIRCB0XES = 5;

const int N_PAULIS = 4;
const int N_INIT_BITS = 2;
const int N_NAMED_BITS = 2;
const float C_GATE_RATIO = 0.3;

const int MAX_NEST_DEPTH = 3;
const int MAX_CIRCBOX_REPETITION_CIRC = 3;
const int MAX_NEST_STATEMENTS = 4;

fs::path CIRCUITS_DIR = "quantum_circuits";

std::string paulis[N_PAULIS] = {"X", "Y", "Z", "I"};

/// return a random number given a lower and upper bound (int)
int get_rand(int lb, int ub){

    if(lb <= ub){
        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_int_distribution<> dis(lb, ub);

        int random_number = dis(gen);
        
        return random_number;
    }
    else{
        std::cerr << "Lb is greater than ub" << std::endl;
        return 0;
    }
}

/// return a random number between lower and upper bound (float)
float f_get_rand(float lb, float ub){
    float denominator = 1000.0;
    int i_lb = lb * denominator;
    int i_ub = ub * denominator;

    return (float)get_rand(i_lb, i_ub) / denominator;
}

std::bitset<4> numtobin(U4& number){
    std::bitset<4> binaryRepresentation(number);

    return binaryRepresentation;
}

std::vector<std::string> qiskit_opt_passes = {"Optimize1qGates", "Optimize1qGatesDecomposition", "Collect1qRuns", "Collect2qBlocks",
    "CollectMultiQBlocks","CollectLinearFunctions","CollectCliffords","ConsolidateBlocks","CXCancellation","InverseCancellation",
    "CommutationAnalysis","CommutativeCancellation","CommutativeInverseCancellation","Optimize1qGatesSimpleCommutation","RemoveDiagonalGatesBeforeMeasure",
    "RemoveResetInZeroState","RemoveFinalReset","HoareOptimizer","TemplateOptimization","ResetAfterMeasureSimplification",
    "OptimizeCliffords","ElidePermutations","NormalizeRXAngle","OptimizeAnnotated", "AllOpt"
};

std::vector<std::string> cirq_all_passes = {"stratified_circuit","merge_single_qubit_gates_to_phased_x_and_z","merge_single_qubit_gates_to_phxz",
    "merge_single_qubit_moments_to_phxz","merge_k_qubit_unitaries","expand_composite","eject_z", "eject_phased_paulis",
    "add_dynamical_decoupling","drop_negligible_operations","drop_empty_moments","align_left", "align_right"};

std::vector<std::string> cirq_target_gatesets = {"cz(allow_partial=True)", "cz(allow_partial=False)", "sqrtiswap"};

std::vector<std::string> cirq_insert_strats = {"InsertStrategy.NEW", "InsertStrategy.NEW_THEN_INLINE", "InsertStrategy.INLINE", "InsertStrategy.EARLIEST"};
