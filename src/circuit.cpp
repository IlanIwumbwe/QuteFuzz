#include "../headers/circuit.h"

/// @brief If `flag` is set, a qubit resource will be returned, otherwise, a bit resource is returned
/// @param flag 
/// @return 
Resource* circuit_info::choose_random_resource(bool flag){
    if(flag){
        assert(available_qubit_resources.size() > 0);
        return &available_qubit_resources[get_rand(0, get_total_qubits()-1)];
    } else {
        assert(available_bit_resources.size() > 0);
        return &available_bit_resources[get_rand(0, get_total_bits()-1)];
    }
}

void circuit_info::write_param_bindings(std::ofstream& stream){
    stream << "bindings = {";
    for(Param& p : defined_symbols){
        if(p.used){
            stream << p.name << ": " << p.val << ", ";
        }
    }

    stream << "}" << std::endl;
}

void circuit_info::set_gateset_by_pass(){
    size_t init_size = cr->gateset.size();
    
    if(init_size == 0){
        for(Gate& g : ALL_SUPPORTED_GATES){
            if(g.type & cr->gateset_flag){
                cr->gateset.push_back(g);
                init_size++;
            }
        }
    }

    gateset = get_subset_of_gateset(cr->gateset, 0.3);

    int two_q_gates = 0, pgates = 0;

    #ifdef DEV 
        std::cout << "=====================================================" << std::endl;
        std::cout << "SWARM gateset; initial: " << init_size << " swarm size: " << gateset.size() << std::endl;
    #endif

    for(Gate g : gateset){
        #ifdef DEV
            std::cout << g;
        #endif
        
        if(g.type & two_qubit_gate){
            two_q_gates += 1;
            uses_control_gates = true;
        } else if(g.type & primitive){
            pgates += 1;
        } else if (g.type & n_control_gates_added){
            uses_control_gates = true;
        }
    }

    #ifdef DEV
        std::cout << "=====================================================" << std::endl;
    #endif

    ULL type_to_get;

    if(two_q_gates >= pgates){
        type_to_get = two_qubit_gate;
        multiplexor_states = std::min(4, two_q_gates);
    } else {
        type_to_get = primitive;
        multiplexor_states = std::min(4, pgates);
    }

    if(multiplexor_states && !(multiplexor_states % 2) && !(cr->restriction & no_mult)){
        can_have_multiplexor = true;
        set_multiplexor_ops(type_to_get);
    }
}

void circuit_info::set_multiplexor_ops(ULL type_to_get){
    Gate g;

    while(multiplexor_ops.size() < (size_t)multiplexor_states){
        g = gateset[get_rand(0, gateset.size()-1)];
    
        if(g.type & type_to_get){	
            multiplexor_ops.push_back(g);
        }
    }
}

std::ostream& operator<<(std::ostream& os, circuit_info& info){
    std::string type = ((info.circ_kind == subroutine) ? "[CIRCBOX : " + info.name + "]" : "[INF0]");
    os << "========================================================================" << std::endl;

    os << type << " Number of qubits " << info.get_total_qubits() << std::endl;
    os << type << " Number of gates " << info.n_gates_to_add << std::endl;
    os << type << " Number of control gates " << info.n_control_gates_added << std::endl;
    os << type << " Available resources: \n";

    for(Resource r : info.available_qubit_resources){
        os << r;
    }

    for(Resource r : info.available_bit_resources){
        os << r;
    }

    os << "========================================================================" << std::endl;

    return os;
}