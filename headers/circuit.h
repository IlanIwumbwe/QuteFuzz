#ifndef CIRCUIT_H
#define CIRCUIT_H

#include <string>
#include "gate.h"
#include "resource.h"

typedef enum {
	subroutine,
	main_circ
} circuit_kind;

struct circuit_info{
	std::string name;
	Circuit_Restrictions* cr;

	int n_init_qubits = 0;
	int n_init_bits = 0;
	int n_gates_to_add = 0;
	int n_control_gates_to_add = 0;

	int n_named_qubits = 0;
	int n_named_bits = 0;

	int n_control_gates_added = 0;
	int n_total_gates_added = 0;

	int n_subroutines = get_rand(0, MAX_CIRCB0XES);

	int multiplexor_states = 0;

	circuit_kind circ_kind = main_circ;

	/// @brief These are strictly symbols that are defined within the circuit
	std::vector<Param> defined_symbols;

	std::vector<Resource> available_qubit_resources;
	std::vector<Resource> available_bit_resources;

	std::vector<Gate> multiplexor_ops;

	bool can_have_conditionals = false;
	bool can_have_multiplexor = false;
	bool uses_control_gates = false;
	
	/// @brief Gateset used to generate a circuit/subcircuit
	std::vector<Gate> gateset;

	std::string indent = "";
	int nest_depth =  ((f == f_qiskit) && get_rand(0,1)) ? get_rand(1, MAX_NEST_DEPTH) : 0;

	circuit_info(){}

	circuit_info(std::string n, circuit_kind k, Circuit_Restrictions* _cr){
		assert(k == main_circ);

		name = n;
		circ_kind = k;
		cr = _cr;

		set_gateset_by_pass();

		can_have_conditionals = true;

		n_gates_to_add = get_rand(MIN_TOTAL_GATES, MAX_TOTAL_GATES);
		n_control_gates_to_add = n_gates_to_add * C_GATE_RATIO;
	}

	circuit_info(std::string n, circuit_kind k, std::vector<Gate> g){
		assert(k == subroutine);

		name = n;
		circ_kind = k;
		gateset = g;

		n_init_qubits = 0;
		n_named_qubits = MAX_ADDED_CIRCBOX_QUBITS;
		n_gates_to_add = get_rand(MIN_CIRCBOX_GATES, MAX_CIRCBOX_GATES);
	}

	/// Add to available qubit resources, if this is not init qubits, increment added qubits counter
	void add_qubit_resources(Resource r){
		available_qubit_resources.push_back(r);
	}

	/// Add to available bit resources, if this is not init bits, increment added bits counter
	void add_bit_resources(Resource r){
		available_bit_resources.push_back(r);
	}

	Resource* choose_random_resource(bool flag);

	/// @brief Reset used flags for all bit and qubit resources
	void reset_resource_flags(){
		for(Resource& r : available_qubit_resources){
			r.used = false;
			r.bad_choice_for_replacement = false;
		}

		for(Resource& r : available_bit_resources){
			r.used = false;
			r.bad_choice_for_replacement = false;
		}
	}

	void reset_choices_flags(){

	}

	void reset_state(){
		available_qubit_resources.clear();
		available_bit_resources.clear();

		n_control_gates_added = 0;
		n_total_gates_added = 0;
	}
	
	/// @brief Gets a random gate from the gateset.
	/// If this circuit has control gates and hasn't fulfilled the quota yet, return only control gates so that it does
	/// @return 
	Gate* get_random_gate(){
		Gate* g = &gateset[get_rand(0, gateset.size()-1)];

		if(uses_control_gates && (circ_kind == main_circ) && (n_control_gates_added < n_control_gates_to_add) && (n_total_gates_added >= (n_gates_to_add * (1-C_GATE_RATIO)))){
			while(!(g->type & (two_qubit_gate | n_qubit_gate) & ~circbox)){
				g = &gateset[get_rand(0, gateset.size()-1)];
			}
		}

		return g;
	}

	Param* get_random_symbol(){
		return &defined_symbols[get_rand(0, defined_symbols.size()-1)];
	}

	void write_param_bindings(std::ofstream& stream);

	friend std::ostream& operator<<(std::ostream& os, circuit_info& info);

	int get_total_qubits(){
		return n_init_qubits + n_named_qubits;
	}

	int get_total_bits(){
		return n_init_bits + n_named_bits;
	}

	void set_gateset_by_pass();

	void set_multiplexor_ops(ULL type_to_get);

	void indent_one_level(){
		indent += "\t";
	}

	void unindent_one_level(){
		if(indent.length()){indent.pop_back();}
	}

};


#endif