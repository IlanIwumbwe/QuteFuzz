#ifndef GATE_H
#define GATE_H

#include "utils.h"
#include "param.h"
#include "resource.h"

/// @brief Name, num_of_args, num_of_resources
struct Gate{
	std::string name;
	int num_of_resources = 0;
	int num_of_gates = 1;
	int num_of_control_gates = 0;

	gate_type type;
	bool q_flag = true;
	bool in_subset = false;
	bool used = false;
	bool mult_suitable = true;

	std::vector<Param> args = {};
	std::vector<Resource> resources_used {};

	std::string starter, r_s = "", r_e = "", a_s = "", a_e = "";

	Gate(){}

	Gate(std::string n, std::vector<Param> ga, int resources, gate_type t){
		name = n; args = ga; num_of_resources = resources; type = t;
		set_vars();  
	}

	Gate(std::vector<Param> ga, int resources, gate_type t){
		args = ga; num_of_resources = resources; type = t;
		name = get_gate_name(type);
		set_vars();  
	}

	Gate(int resources, gate_type t){
		num_of_resources = resources; type = t;
		name = get_gate_name(type);
		set_vars();
	}

	Gate(int resources, int n_gates, gate_type t){
		num_of_resources = resources;
		num_of_gates = n_gates;
		type = t;
	}

	void set_vars(){	
		int num_of_args = args.size();	

		if(num_of_args){
			if(f == f_cirq){
				a_e = ").on(";
			} else {
				a_e = ", ";
			}
		}

		if(type & (multiplexor | circbox)) {
			if(f == f_pytket){
				starter = ".add_gate(" + name + ",";
			} else {
				starter = ".append(" + name + ",";
			}

			r_s = "[";
			r_e = "]";

			if(num_of_args){
				a_e = "),";
				a_s = "(";
			}
		} else if (type & paulibox){
			starter = ".add_gate(" + name;
			r_s = "[";
			r_e = "]";

		} else if ((type & pytket_optype) && (f == f_pytket)){
			starter = ".add_gate(OpType." + name + ",";
			r_s = "[";
			r_e = "]";

			if(num_of_args){
				a_e = "),";
				a_s = "(";
			}

		} else if (type & unitary_box){
			starter = ".add_unitary" + std::to_string(num_of_resources) + "qbox(" + name + ",";

		} else { 
			if(f == f_cirq){
				starter = ".append(" + name + "(";
				r_e = ")";
			} else {
				starter = "." + name + "(";
			}

		}

		if(type & (two_qubit_gate | n_qubit_gate)){
			num_of_control_gates = 1;
		}
	}

	friend std::ostream& operator<<(std::ostream& os, Gate gate){
		os << "=====================================================" << std::endl;
		os << "|	Gate name " << gate.name << std::endl;
		os << "|	Num of args " << gate.args.size() << std::endl;
		os << "|	Num of resources " << gate.num_of_resources << std::endl;
		os << "|	Num of gates " << gate.num_of_gates << std::endl;
		os << "|	Num of control gates " << gate.num_of_control_gates << std::endl;
		os << "=====================================================" << std::endl;

		return os;
	}

	bool operator==(Gate g){
		return (name == g.name) && (type == g.type) && (q_flag == g.q_flag);
	}
};

#endif