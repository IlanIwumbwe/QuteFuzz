#include "../headers/utils.h"
#include <iostream>

fs::path CIRCUITS_DIR = "quantum_circuits";
frontend f = f_pytket;

struct gate_name_mapping{
    gate_type t;
    std::string name[SUPPORTED_FRONTENDS];
};

/// @brief Empty strings imply that the gate doesn't exist for that front end. This gate type will never be used by that front-end anyway
const std::vector<gate_name_mapping> GATE_NAMES = {
    {noop, {"noop", "noop", ""}},
    {cy, {"CY", "cy", ""}},
    {multiplexor, {"multiplexor", "multiplexor"}},
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
    {cz, {"CZ", "cz", "CZ"}},
    {s, {"S", "s", "S"}},
    {cnx, {"CnX", "cnx", ""}},
    {cny, {"CnY", "cny", ""}},
    {cnz, {"CnZ", "cnz", ""}},
    {cnrx, {"CnRx", "cnrx", ""}},
    {cnry, {"CnRy", "cnry", ""}},
    {cnrz, {"CnRz", "cnrz", ""}},
    {cnrx, {"CRx", "crx", ""}},
    {cnry, {"CRy", "cry", ""}},
    {crz, {"CRz", "crz", ""}},
    {xxphase, {"XXPhase", "yyphase", ""}},
    {yyphase, {"YYPhase", "yyphase", ""}},
    {zzphase, {"ZZPhase", "zzphase", ""}},
    {h, {"H", "h", ""}},
    {rx, {"Rx", "rx", "rx"}},
    {ry, {"Ry", "ry", "ry"}},
    {rz, {"Rz", "rz", "ry"}},
    {sx, {"", "sx", ""}},
    {paulibox, {"pauli_box", "pauli_box"}},
    {u, {"", "u", ""}},
    {t, {"","","T"}},
    {cswap, {"","","CSWAP"}},
    {phasedxz, {"","","PhasedXZGate"}},
    {phasedxpow, {"","","PhasedXPowGate"}}
};



std::bitset<4> numtobin(U4& number){
    std::bitset<4> binaryRepresentation(number);

    return binaryRepresentation;
}

/// @brief Given a gate type flag, return the name of that gate as a string depending on frontend being generated
/// @param t 
/// @return 
std::string get_gate_name(gate_type t){
    for(size_t i = 0; i < GATE_NAMES.size(); ++i){
        if(GATE_NAMES[i].t == t){
            return GATE_NAMES[i].name[f];
        }
    }

    std::cerr << "Gate type 2^" << get_lsb(t) << " doesn't have a defined name!" << std::endl;
    exit(-1);
}

