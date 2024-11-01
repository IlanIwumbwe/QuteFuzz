
#include "../headers/generator.h"

std::vector<Gate> ALL_SUPPORTED_GATES{};

/// @brief Get n resources of any type
/// @param info 
/// @param n 
/// @param chosen_resources 
/// @param rt
/// @return true / false based on whether you could successfully get n qubits 
bool get_any_qubits(circuit_info& info, int n, std::vector<Resource>& chosen_resources){
	info.reset_resource_flags();

	chosen_resources.clear();

	Resource* r;

	if((int)info.available_qubit_resources.size() >= n){
		while((int)chosen_resources.size() != n){
			r = info.choose_random_resource(true);

			#ifdef DEV
				std::cout << "chosen r " << r->str << std::endl;
			#endif
		
			if(!r->used){
				r->used = true;
				r->times_used += 1;
				chosen_resources.push_back(*r);
			}
		}

		return true;
	}

	return false;
}

/// @brief Given a gate that uses n resources, populate the resources vector with distict resources for it to use
/// Similar qubits means that all qubits will be named, or all will be indices
/// @param info 
/// @param gate 
/// @param chosen_resources 
/// @return true or false depending on whether this is possible
bool get_n_similar_qubits(circuit_info& info, int n, std::vector<Resource>& chosen_resources){
	info.reset_resource_flags();

	chosen_resources.clear();

	Resource* r = info.choose_random_resource(true);
	r->used = true;
	r->times_used += 1;

	chosen_resources.push_back(*r);

	#ifdef DEV
		std::cout << "first " << r->str << std::endl;
	#endif

	// check if first random resource was index, if so, make sure you have enough initial qubits to satisfy n
	if(r->rt == index){
		if(info.n_init_qubits < n){
			r->used = false;
			r->times_used -= 1;
			return false;

		} else {
			// need to satisfy all n resources with index resources
			get_particular_qubits(info, n, chosen_resources, index);
			return true;
		}

	} else {

		if(info.n_named_qubits < n){
			r->used = false;
			r->times_used -= 1;
			return false;

		} else {
			// first resource was a named qubit
			// need to satisfy all n resources with non-index resources
			get_particular_qubits(info, n, chosen_resources, named);
			return true;
		}
	}
}

/// @brief Get n resources of a particular type
/// @param info 
/// @param n 
/// @param chosen_resources 
/// @param rt 
void get_particular_qubits(circuit_info& info, int n, std::vector<Resource>& chosen_resources, resource_type rt){
	Resource* r;

	while((int)chosen_resources.size() != n){
		r = info.choose_random_resource(true);

		#ifdef DEV
			std::cout << "next " << r->str << std::endl;
		#endif

		if(!r->used && (r->rt == rt)){
			r->used = true;
			r->times_used += 1;
			chosen_resources.push_back(*r);
		}
	}
}

void write_gate(std::ofstream& stream, circuit_info& info, Gate& g, std::string special_options, std::string special_modifications){
	stream << info.indent + info.name + g.starter;

	write_args(stream, info, g);
	write_resources(stream, g);
	
	stream << special_modifications + special_options;

	#ifdef DEV
		std::cout << g;
	#endif

	info.n_control_gates_added += g.num_of_control_gates;
	info.n_total_gates_added += g.num_of_gates;
}

int apply_gate(std::ofstream& stream, circuit_info& info, Gate& g, bool (*resource_getter)(circuit_info&, int, std::vector<Resource>&)){

	if((info.n_total_gates_added + g.num_of_gates <= info.n_gates_to_add) && resource_getter(info, g.num_of_resources, g.resources_used)){
		write_gate(stream, info, g);
		stream << ")" << std::endl;
		return g.num_of_gates;
	
	} else {
		return 0;
	}
}

void write_resources(std::ofstream& stream, Gate& gate){
	int added_resources = 0;

	stream << gate.r_s;

	// add resources
	for(Resource r : gate.resources_used){
		added_resources += 1;
		
		if(added_resources == gate.num_of_resources){
			stream << r.str;
		} else {
			stream << r.str << ",";
		}
	}

	stream << gate.r_e;
}

void add_symbols(std::ofstream& stream, circuit_info& info) {
	stream << "# Adding symbols " << std::endl;

	std::string prefix = "param";

	for (int i = 0; i < get_rand(1, 10); ++i) {
		Param p(prefix + "_" + std::to_string(i));

		stream << p.name << " = " << p.definition_keyword << "(\"" << p.name << "\")" << std::endl;
		info.defined_symbols.push_back(p);
	}

	stream << "\n"; 
}

void write_args(std::ofstream& stream, circuit_info& info, Gate& gate){
	std::string argdelim = ",";
	Param* p;
	int choose_symbol;
			
	stream << gate.a_s;

	// add arguments
	for(size_t i = 0; i < gate.args.size(); ++i){
		p = &gate.args[i];
		choose_symbol = get_rand(0, 1);

		if(i == gate.args.size()-1){argdelim = "";}

		if(choose_symbol && info.defined_symbols.size()){
			p = info.get_random_symbol();
			p->used = true;
			stream << p->name << argdelim;
		} else if (p->val == ""){
			stream << p->name << std::to_string(f_get_rand(-1.0, 1.0)) << argdelim;
		} else {
			stream << p->name << p->val << argdelim;
		}
	}

	stream << gate.a_e;
}

std::vector<Gate> get_r_of_vec(std::vector<Gate> vec, float ratio){
	assert(vec.size() > 0);

	size_t size = ratio * vec.size();

	if(size > 1){
		std::vector<Gate> subset;
		Gate* g = &vec[get_rand(0, vec.size()-1)];
		
		g->in_subset = true;
		subset.push_back(*g);

		while(subset.size() < size){
			g = &vec[get_rand(0, vec.size()-1)];

			if(!g->in_subset){
				g->in_subset = true;
				subset.push_back(*g);
			}
		}

		return subset;

	} else {
		return vec;
	}
}

template<typename T>
void v_append(std::vector<T>& v1, std::vector<T>& v2){
    v1.insert(v1.end(), v2.begin(), v2.end());
}

template<typename T>
bool v_exists(std::vector<T> vec, T val){
	return std::find(vec.begin(), vec.end(), val) != vec.end();
}

void generate(int n){
	
	ALL_SUPPORTED_GATES = {
		Gate{1,x}, Gate{1,y},Gate{1, z}, Gate{1,v}, Gate{{Param()}, 1,u1}, Gate{{Param("","pi/2"),Param(),Param()},1,u}, 
		Gate{{Param("","0"),Param("","0"),Param()},1,u}, Gate{{Param(),Param(),Param()},1,u}, Gate{1,t},
		Gate{{Param(),Param(),Param()},1,u3}, Gate{{Param(),Param()},1, u2}, Gate{2, swap}, Gate{{Param(),Param(),Param()},1, tk1}, Gate{3,cswap},
		Gate{{Param(),Param(),Param()},2, tk2}, Gate{2, cx}, Gate{2,cy}, Gate{2, cz},
		Gate{2, cnx}, Gate{2, cny}, Gate{1, s}, Gate{1,sx},
		Gate{2, cnz}, Gate{3, cnx}, Gate{1, noop},
		Gate{3, cny}, Gate{3, cnz}, Gate{{Param("phase_exponent=")},1,phasedxpow},
		Gate{4, cnx}, Gate{4, cny}, Gate{{Param("x_exponent="),Param("axis_phase_exponent="),Param("z_exponent=")},1,phasedxz},
		Gate{4, cnz}, Gate{{Param()},2, cnrx}, 
		Gate{{Param()},2, cnry}, Gate{{Param()},2,cnrz}, 
		Gate{{Param()},3, cnrx}, Gate{{Param()},3, cnry}, 
		Gate{{Param()},3, cnrz}, Gate{{Param()},4, cnrx}, 
		Gate{{Param()},4, cnry},Gate{{Param()},4, cnrz},
		Gate{{Param()},2, xxphase}, Gate{{Param()},2,yyphase}, Gate{{Param()},2,zzphase},
		Gate{1, h}, Gate{{Param()},1,rz},
		Gate{{Param()},1,rx}, Gate{{Param()},1,ry}, 
	};

	if(f == f_qiskit){
		qiskit::generate_circuits(n);
	} else if (f == f_pytket){
		pytket::generate_circuits(n);
	} else if (f == f_cirq){
		cirq::generate_circuits(n);
	}

}