#ifndef GATE_H
#define GATE_H

#include "utils.h"
#include "resource.h"

typedef enum {
	noop = set_bit(0),
	cy = set_bit(1),
	multiplexor = set_bit(2),
	circbox = set_bit(3),
	paulibox = set_bit(4),

	ry = set_bit(6),

	unitary_box = set_bit(8),

	cnx = set_bit(11),
	tk1 = set_bit(12),
	tk2 = set_bit(13),
	cx = set_bit(14),
	cz = set_bit(15),
	swap = set_bit(16),
	rx = set_bit(17),
	rz = set_bit(18),
	h = set_bit(19),
	x = set_bit(20),
	z = set_bit(21),
	y = set_bit(22),
	v = set_bit(23),
	s = set_bit(24),
	u1 = set_bit(25),
	u2 = set_bit(26),
	u3 = set_bit(27),
	cny = set_bit(28),
	cnz = set_bit(29),
	cnrx = set_bit(30),
	cnry = set_bit(31),
	cnrz = set_bit(32),
	xxphase = set_bit(33),
	yyphase = set_bit(34),
	zzphase = set_bit(35),
	sx = set_bit(36),
	u = set_bit(37),
	crx = set_bit(38),
	cry = set_bit(39),
	crz = set_bit(40),
	t = set_bit(41),
	cswap = set_bit(42),
	phasedxz = set_bit(43),
	phasedxpow = set_bit(44),

} gate_type;

#define primitive (x | y | z | h | s | u3 | u2 | u1)
#define control_rotation (crx | cry | crz)
#define control (cx | cy | cz)
#define two_qubit_gate (control | swap | control_rotation) 
#define rotation (rx | ry | rz)
#define clifford (h | cx | rz)
#define phased (xxphase | yyphase | zzphase)
#define pytket_optype (noop | cny | cnx | cnz | cnrx | cnry | cnrz | phased)
#define n_qubit_gate (cny | cnx | cnz | cnrx | cnry | cnrz)
#define qiskit_flags (x | y | z | h | s | u | control | rotation | control_rotation)
#define cirq_flags (x | y | z | rx | ry | rz | s | t | cswap | phasedxz | phasedxpow | cx | cz)

std::string get_gate_name(gate_type t);

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

struct Circuit_Restrictions{
	std::string name;
	ULL gateset_flag;
	unsigned int restriction = 0;
	std::vector<Gate> gateset;

	Circuit_Restrictions(){}
	Circuit_Restrictions(std::string n, ULL gsf) : name(n), gateset_flag(gsf){}
	Circuit_Restrictions(std::string n, ULL gsf, unsigned int r) : name(n), gateset_flag(gsf), restriction(r){}
};

struct gate_mapping{
	gate_type t;
	const char* names[SUPPORTED_FRONTENDS];
};

std::vector<Gate> get_r_of_vec(std::vector<Gate> vec, float ratio);
extern std::vector<Gate> ALL_SUPPORTED_GATES;
extern std::vector<Circuit_Restrictions> pytket_opt_passes;

#endif