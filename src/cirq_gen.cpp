#include "../headers/generator.h"

int cirq::measures = 0;

std::vector<std::string> cirq::all_passes = {"stratified_circuit","merge_single_qubit_gates_to_phased_x_and_z","merge_single_qubit_gates_to_phxz",
    "merge_single_qubit_moments_to_phxz","merge_k_qubit_unitaries","expand_composite","eject_z", "eject_phased_paulis",
    "add_dynamical_decoupling","drop_negligible_operations","drop_empty_moments","align_left", "align_right"};

std::vector<std::string> cirq::target_gatesets = {"cz(allow_partial=True)", "cz(allow_partial=False)", "sqrtiswap"};

std::vector<std::string> cirq::insert_strats = {"InsertStrategy.NEW", "InsertStrategy.NEW_THEN_INLINE", "InsertStrategy.INLINE", "InsertStrategy.EARLIEST"};

void cirq::write_imports(std::ofstream& stream, circuit_info& info){

	stream << "from cirq import (Circuit, ";

    // go through the gateset and import the gates this circuit will use

    for(Gate& g : info.gateset){
        stream << g.name << ", ";
    }

    stream << "\n\tNamedQubit, InsertStrategy, CircuitOperation, measure)" << std::endl;
    stream << "from pathlib import Path" << std::endl;
	stream << "from helpers.cirq_helpers import compare_circuits, individual_pass" << std::endl;
	stream << "\n";
}

void cirq::add_resources(std::ofstream& stream, circuit_info& info){
    Resource r;
	std::string qreg_name;
	int qreg_size;
	r.rt = named;

	stream << "# Adding qubits " << std::endl;

	qreg_name = "qubits";
	qreg_size = info.n_named_qubits;

	stream << qreg_name << " = NamedQubit.range(" << qreg_size << ", prefix=\"q\")" << std::endl;
	
	for(int i = 0; i < qreg_size; ++i){
		r.str = qreg_name + "[" + std::to_string(i) + "]";
		info.add_qubit_resources(r); 
	}

    stream << "\n";
}

// measure a qubit state into this bit resource
void cirq::add_measure(std::ofstream& stream, circuit_info& info){
	Resource* qr = info.choose_random_resource(true);

	// make a mid circuit measurement of a qubit into this bit
	stream << info.tab << info.name << ".append(measure(" << qr->str << ", key=\"cbit" << std::to_string(measures) << "\"))" << std::endl;
}

/// @brief Given a gate `g` (subroutine), and a set of available qubits, replace one of the qubits used within the subroutine with another qubit.
/// Need to check that this replacement will not clash with other internal gates i.e. 2 qubit gates ending up with the same qubit as input 
/// @param stream
/// @param choices
/// @param g 
/// @return nothing
void cirq::write_qubit_replacement(std::ofstream& stream, circuit_info& info, Gate& g){

	if((info.circ_kind == main_circ) && get_rand(0, 1) && g.resources_used.size()){
		int num_of_choices = info.get_total_qubits();
		int pos_of_old_qubit = get_rand(0, g.resources_used.size()-1), pos_of_replacement = get_rand(0, num_of_choices-1), index = 0;

		Resource old_qubit = g.resources_used[pos_of_old_qubit], concurrent_qubit;
		Resource* new_qubit = &info.available_qubit_resources[pos_of_replacement];

		while(old_qubit == *new_qubit){
			pos_of_replacement = get_rand(0, num_of_choices-1);
			new_qubit = &info.available_qubit_resources[pos_of_replacement];
		}

		int choices_tried = 1;

		std::vector<Resource> v_ccr = old_qubit.concurrent_resources;

		bool found = (v_ccr.size() == 0);		

		while(!found && (choices_tried < num_of_choices)){
			concurrent_qubit = v_ccr[index];

			if(concurrent_qubit == *new_qubit){
				// this new_qubit was a bad choice and shouldn't be tried again
				new_qubit->bad_choice_for_replacement = true;
				
				while(new_qubit->bad_choice_for_replacement){
					pos_of_replacement = get_rand(0, num_of_choices-1); 
					new_qubit = &info.available_qubit_resources[pos_of_replacement];
				}

				choices_tried += 1;

				index = 0;
			} else {
				index += 1;
				if(index == (int)v_ccr.size()){found = true;}
			}
		}

		if(found){
			stream << ".with_qubit_mapping({" << old_qubit.str << ": " << new_qubit->str << "})";

			// if within a subroutine, all qubit concurrency information from the old qubit is transferred to the new qubit
			if(info.circ_kind == subroutine){
				new_qubit->get_concurrencies(old_qubit);
			}
		
		} 
		
		#ifdef DEV
			std::cout << "Could not find any replacement qubits" << std::endl;
		#endif

	}
		
	#ifdef DEV
		std::cout << "Chose not to add qubit mapping" << std::endl;
	#endif
	
}

/// @brief For all qubit resources in this circuit that are the same as qubit resources used within this subroutine gate, 
/// transfer all concurrency information from the qubit within the subroutine gate its counterpart in the circuit  
/// @param info 
void cirq::transfer_concurrencies(circuit_info& info, Gate& g){
	assert(g.type == circbox);

	for(Resource& circ_r : info.available_qubit_resources){
		for(Resource& gate_r : g.resources_used){
			if(circ_r == gate_r){
				circ_r.get_concurrencies(gate_r);
			}
		}
	}
}

int cirq::apply_gate(std::ofstream& stream, circuit_info& info, Gate& g){

	int n_repeat = (g.type & circbox) ? get_rand(1, MAX_CIRCBOX_REPETITION) : 1;

	if(info.n_total_gates_added + (n_repeat * g.num_of_gates) <= info.n_gates_to_add){
		// decide whether this circuit should be a conditional
		std::string special_modifications = "";
		
		if((get_rand(1, 10) == 1) && (info.circ_kind != subroutine)) {
			add_measure(stream, info);
			special_modifications = ".with_classical_controls(\'cbit" + std::to_string(measures++) + "\')";
		}

		#ifdef DEV 
			std::cout << g; 
		#endif

		if(g.type & circbox){
			transfer_concurrencies(info, g);

			info.n_control_gates_added += (n_repeat * g.num_of_control_gates);
			info.n_total_gates_added += (n_repeat * g.num_of_gates);

			stream << info.tab + info.name + ".append(" + g.name << ".repeat(" << n_repeat << ")";

			write_qubit_replacement(stream, info, g);	

			stream << special_modifications << ")" << std::endl;

		} else if (get_any_qubits(info, g.num_of_resources, g.resources_used)){

			std::string insert_strat = insert_strats[get_rand(0, insert_strats.size()-1)];
		
			write_gate(stream, info, g, ", strategy = " + insert_strat, special_modifications);

			stream << ")" << std::endl;
		}

		return n_repeat * g.num_of_gates;
	}

	return 0;
}

void cirq::apply_gates(std::ofstream& stream, circuit_info& info){
    Gate* gate;

	while(info.n_total_gates_added < info.n_gates_to_add){
		gate = info.get_random_gate();
		apply_gate(stream, info, *gate);
	}

	info.unindent();
}

void cirq::write_circboxes(std::ofstream& stream, circuit_info& info){
	circuit_info circ("", subroutine, info.gateset);

	// make some number of circboxes
	for(int i = 0; i < info.n_subroutines; ++i){	
		circ.name = "subcirc" + std::to_string(i);

		Gate gate(circ.get_total_qubits(), circ.n_gates_to_add, circbox);
		gate.name = circ.name + "_op";	

		// choose qubit resources that this subroutine can use
		circ.available_qubit_resources.clear();
		get_any_qubits(info, gate.num_of_resources, circ.available_qubit_resources);	

		circ.n_total_gates_added = 0;
		circ.n_control_gates_added = 0;

		write_circuit(stream, circ);

		// keep track of which qubits were used together within the entire subroutine
		// O(n^2) but n is at most 6 so eh
		for(Resource ri : circ.available_qubit_resources){	
			for(Resource rj : circ.available_qubit_resources){
				if(!(ri == rj)){
					ri.concurrent_resources.push_back(rj);
				}
			}
		
			gate.resources_used.push_back(ri);
		}

		gate.num_of_control_gates = circ.n_control_gates_added;
		gate.set_vars();

		stream << gate.name << " = CircuitOperation(" << circ.name << ".freeze())" << std::endl;

		stream << std::endl;

		info.gateset.push_back(gate);  // add back to your parent's gateset
		circ.gateset.push_back(gate); // can have subroutines within other subroutines
	}
}

void cirq::write_circuit(std::ofstream& stream, circuit_info& info){

	stream << info.name << " = Circuit()" << std::endl;

	assert(info.available_qubit_resources.size() == (size_t)info.get_total_qubits());
	assert(info.available_bit_resources.size() == (size_t)info.get_total_bits());

	apply_gates(stream, info);

	#ifdef DEV
		std::cout << info << std::endl;
	#endif
}

void cirq::generate_circuits(int n){
	fs::path circuit_filename;

	if(!fs::exists(CIRCUITS_DIR)){
		fs::create_directory(CIRCUITS_DIR);
	}

	Circuit_Restrictions cr{"Cirq Gateset", cirq_flags};

	for(int i = 0; i < n; ++i){

		#ifdef DEV
			std::cout << "================== circuit" << i+1 << ".py =========================\n" << std::endl;
		#endif

		circuit_filename = CIRCUITS_DIR / ("circuit" + std::to_string(i+1) + ".py");
	
		std::ofstream stream(circuit_filename.c_str());

		circuit_info global_info("main_circ", main_circ, &cr);

		int total_qubits = get_rand(MIN_TOTAL_QUBITS, MAX_TOTAL_QUBITS);

		global_info.n_init_qubits = 0;
		global_info.n_named_qubits = total_qubits;

		write_imports(stream, global_info);

		add_resources(stream, global_info);

        write_circboxes(stream, global_info);

		write_circuit(stream, global_info);

		stream << "\n";
		stream << "print(Path(__file__).name, \" results:\")" << std::endl;
		stream << "main_circ.append(measure(qubits, key=\"results\"))" << std::endl;

		if (get_rand(0, 1)) {
			stream << "individual_pass(" << global_info.name << ", " << i+1 << ", \"" << all_passes[i%(int)all_passes.size()] << "\")" << std::endl;
		} else {
			stream << "compare_circuits(" << global_info.name << ", \"" << target_gatesets[i%target_gatesets.size()] << "\","<< i+1 << ")" << std::endl;
		}

		//Resets name every different circuit
		measures = 0;
		stream.close();
	}
}