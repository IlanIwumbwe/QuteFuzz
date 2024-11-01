
#include "../headers/generator.h"

void pytket::write_imports(std::ofstream& stream, unsigned int restriction){
	stream << 
	"from sympy import Symbol\n"
	"from helpers.pytket_helpers import test_circuit_on_passes\n"
	"from pathlib import Path\n"
	
	"from pytket import Circuit, Qubit";
	if (!(restriction & no_bits)) {
		 stream << ", Bit";
	}

	stream << "\nfrom pytket.circuit import Op, OpType";
	if (!(restriction & no_circbox)) {
		stream << ", CircBox";
	}
	if (!(restriction & no_mult)) {
		stream << ", MultiplexorBox";
	}
	if (!(restriction & no_paulibox)) {
		stream << ", PauliExpBox, Pauli";
	}
	// stream << "\nfrom pytket.circuit.logic_exp import reg_eq\n\n";

	stream << "\n\n";
}	

void pytket::add_resources(std::ofstream& stream, circuit_info& info){
	Resource r;
	std::string qreg_name, creg_name;
	int qreg_size, creg_size, added_resources = 0;
	r.rt = named;

	stream << "# Adding qregs and qubit resources " << std::endl;

	// fill up available qubit resources with random selection of qubits or qregs
	while(added_resources < info.n_named_qubits){
		if(get_rand(0, 1)){
			// add named qubit resource
			r.str = "qbit_" + std::to_string(added_resources);
			info.add_qubit_resources(r);

			stream << r.str << " = Qubit(\"" << r.str << "\", 0)" << std::endl;
			stream << info.name << ".add_qubit(" << r.str << ")" << std::endl;

			added_resources += 1;
		} else {
			// add qreg resource
			qreg_name = "qreg_" + std::to_string(added_resources);
			qreg_size = get_rand(1, info.n_named_qubits - added_resources);

			r._reg = std::make_pair(qreg_name, qreg_size);

			stream << qreg_name << " = " << info.name << ".add_q_register(\"" << qreg_name << "\"," << qreg_size << ")" << std::endl;

			for(int i = 0; i < qreg_size; ++i){
				r.str = qreg_name + "[" + std::to_string(i) + "]";
				info.add_qubit_resources(r); 
			}

			added_resources += qreg_size;
		}
	}

	added_resources = 0;

	stream << "# Adding creg resources " << std::endl;

	// fill up available bit resources with creg resources
	while(added_resources < info.n_named_bits){
		// add qreg resource
		creg_name = "creg_" + std::to_string(added_resources);
		creg_size = get_rand(1, info.n_named_bits - added_resources);
		
		r._reg = std::make_pair(creg_name, creg_size);

		stream << creg_name << " = " << info.name << ".add_c_register(\"" << creg_name << "\"," << creg_size << ")" << std::endl;

		for(int i = 0; i < creg_size; ++i){
			r.str = creg_name + "[" + std::to_string(i) + "]";
			info.add_bit_resources(r); 
		}

		added_resources += creg_size;
	}
}

void pytket::write_circuit(std::ofstream& stream, circuit_info& info){		

	info.reset_state();

	// init qubit resources (index)
	for(int i = 0; i < info.n_init_qubits; ++i){
		info.add_qubit_resources(Resource{index, std::to_string(i)});
	}

	// subroutines do not use bit resources
	if(info.circ_kind == subroutine){
		stream << info.name << " = Circuit(" << info.n_init_qubits << ", \"" << info.name << "\")" << std::endl;
	} else {
		// init bit resources (index)
		for(int i = 0; i < info.n_init_bits; ++i){
			info.add_bit_resources(Resource{index, "Bit(" + std::to_string(i) + ")"});
		}

		stream << info.name << " = Circuit(" << info.n_init_qubits << ", " << info.n_init_bits << ", \"" << info.name << "\")" << std::endl;
	}
	
	// choose random number of bits and qubits
	add_resources(stream, info);

	assert(info.available_qubit_resources.size() == (size_t)info.get_total_qubits());
	assert(info.available_bit_resources.size() == (size_t)info.get_total_bits());

	if(info.circ_kind == main_circ){
		add_symbols(stream, info);
	}

	stream << "# Applying gates " << std::endl;

	apply_gates(stream, info);

	#ifdef DEV
		std::cout << "Actually applied " << info.n_total_gates_added << std::endl;
	#endif

	if((info.circ_kind == main_circ)){
		info.write_param_bindings(stream);
		stream << info.name << ".symbol_substitution(bindings)\n";
	}

	#ifdef DEV
		std::cout << info << std::endl;
	#endif
}

void pytket::apply_gates(std::ofstream& stream, circuit_info& info){
	Gate* gate;
	
	while(info.n_total_gates_added < info.n_gates_to_add){
		gate = info.get_random_gate();
		apply_gate(stream, info, *gate, get_n_similar_qubits);
	}

	info.unindent_one_level();

}

void pytket::write_circboxes(std::ofstream& stream, circuit_info& info){
	circuit_info circ("", subroutine,  info.gateset);
	
	for(int i = 0; i < info.n_subroutines; ++i){	
		circ.name = "subcirc" + std::to_string(i);

		Gate gate(circ.get_total_qubits(), circ.n_gates_to_add, circbox);
		gate.name = circ.name;	

		write_circuit(stream, circ);

		gate.num_of_control_gates = circ.n_control_gates_added;
		gate.set_vars();

		stream << gate.name << " = CircBox(" << circ.name << ")" << std::endl;

		stream << std::endl;

		info.gateset.push_back(gate);  // add back to your parent's gateset
		circ.gateset.push_back(gate);  // can have subroutines within subroutines	
	}
}

void pytket::generate_circuits(int n){
	fs::path circuit_filename;
	Circuit_Restrictions* cr;
	int circuit_index = 0;

	if(!fs::exists(CIRCUITS_DIR)){
		fs::create_directory(CIRCUITS_DIR);
	}

	while(circuit_index < n){

		#ifdef DEV
			std::cout << "================== circuit" << circuit_index+1 << ".py =========================\n" << std::endl;
		#endif

		circuit_filename = CIRCUITS_DIR / ("circuit" + std::to_string(circuit_index+1) + ".py");
	
		std::ofstream stream(circuit_filename.c_str());

		cr = &pytket_opt_passes[(circuit_index % pytket_opt_passes.size())];

		circuit_info global_info("main_circ", main_circ, cr);

		if(!(cr->restriction & no_bits)){
			global_info.n_init_bits = N_INIT_BITS;
			global_info.n_named_bits = N_NAMED_BITS;
		}

		int total_qubits = get_rand(MIN_TOTAL_QUBITS, MAX_TOTAL_QUBITS);

		if(cr->restriction & no_named_qubits){
			global_info.n_init_qubits = total_qubits;
			global_info.n_named_qubits = 0;
		} else {
			global_info.n_init_qubits = (get_rand(0, 1) ? 4 : total_qubits-4);
			global_info.n_named_qubits = total_qubits - global_info.n_init_qubits;
		}

		write_imports(stream, cr->restriction);

		if(global_info.can_have_multiplexor){
			write_multiplexor(stream, global_info);
		}

		if(!(cr->restriction & no_circbox)){
			write_circboxes(stream, global_info);
		}

		if(!(cr->restriction & no_paulibox)){
			write_pauli_exp(stream, global_info);
		}

		write_circuit(stream, global_info);

		stream << "\n";
		stream << "print(Path(__file__).name, \" results:\")" << std::endl;
		stream << "test_circuit_on_passes(main_circ,\"" << cr->name << "\")" << std::endl;

		stream.close();

		circuit_index++;
	}
}

void pytket::write_multiplexor(std::ofstream& stream, circuit_info& info){
	assert(info.multiplexor_ops.size() > 0);

	int states = info.multiplexor_states, qubits = log2(states);
	Gate mult{"multiplexor", {}, info.multiplexor_ops[0].num_of_resources + qubits, multiplexor};

	std::string bin;

	stream << "# Writing multiplexor " << std::endl;

	for(Gate& g : info.multiplexor_ops){
		stream << g.name << "_op = Op.create(OpType." << g.name << ",";

		g.a_s = "(";
		g.a_e = ")";

		write_args(stream, info, g);

		stream << ")\n";

		mult.num_of_control_gates += g.num_of_control_gates;
	}

	stream << "op_map = {";

	for(U4 i = 0; i < states; ++i){
		bin = numtobin(i).to_string();
		stream << "(";

		for(int i = 4-qubits; i <= 3; ++i){
			stream << std::to_string(bin[i]-'0') + ",";
		}

		stream << "):" << info.multiplexor_ops[i].name + "_op";

		if(i != states-1){
			stream << ",";
		}
	}

	stream << "}" << std::endl;
	
	// multiplexor resources = resources of any one of its ops + num of control qubits needed
	mult.num_of_gates = states;

	info.gateset.push_back(mult);

	stream << "multiplexor = MultiplexorBox(op_map)" << std::endl;
	
	stream << "\n";
}

void pytket::write_pauli_exp(std::ofstream& stream, circuit_info& info){
	int n_paulis = (info.n_named_qubits > 0) ? info.n_named_qubits : info.n_init_qubits;
	int added_paulis = 0;
	std::string pauli_name;
	Gate g{"pauli_box", {Param()}, n_paulis, paulibox};

	stream << "pauli_box = PauliExpBox((";

	while(added_paulis < n_paulis){
		pauli_name = paulis[get_rand(0, N_PAULIS-1)];
		stream << "Pauli." << pauli_name << ", ";
		added_paulis++;
	}

	stream << "), ";

	write_args(stream, info, g); 

	stream << ")\n\n";

	g.args = {};

	info.gateset.push_back(g);
}
