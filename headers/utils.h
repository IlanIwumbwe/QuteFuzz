#ifndef UTILS_H
#define UTILS_H

#include <fstream>
#include <iostream>
#include <random>
#include <assert.h>
#include <filesystem>
#include <bitset>
#include <math.h>
#include <unordered_map>
#include <vector>

#define set_bit(ind) (1ULL << ind)  // return a 64 bit number

namespace fs = std::filesystem;

typedef unsigned char U4;

typedef unsigned long long ULL;

const int SUPPORTED_FRONTENDS = 3;

extern const int MIN_TOTAL_QUBITS;
extern const int MAX_TOTAL_QUBITS;
extern const int MIN_TOTAL_GATES ;
extern const int MAX_TOTAL_GATES ;
extern const int MAX_ADDED_CIRCBOX_QUBITS;
extern const int MIN_CIRCBOX_GATES;
extern const int MAX_CIRCBOX_GATES;
extern const int MAX_CIRCBOX_CONTROL_QUBITS;
extern const int MAX_CIRCB0XES;

extern const int N_PAULIS;
extern const int N_INIT_BITS;
extern const int N_NAMED_BITS;
extern const float C_GATE_RATIO;

extern const int MAX_NEST_DEPTH;
extern const int MAX_CIRCBOX_REPETITION_CIRC;
extern const int MAX_NEST_STATEMENTS;

extern fs::path CIRCUITS_DIR;
extern std::string paulis[4];

extern bool debug;
extern bool plot;

int get_rand(int lb, int ub);

std::bitset<4> numtobin(U4& number);

float f_get_rand(float lb, float ub);

bool is_digit(std::string& s);

template<typename T>
void v_append(std::vector<T>& v1, std::vector<T>& v2);

template<typename T>
bool v_exists(std::vector<T> vec, T val);

typedef enum {
	f_pytket = 0,
	f_qiskit,
	f_cirq,
} frontend;

extern frontend f;

struct Param{
	std::string name = "", definition_keyword = "";
	bool used = false;
	std::string val;

	Param(){}

	Param(std::string n) {
		name = n;
		val = std::to_string(f_get_rand(-1.0, 1.0));

		set_definition_keyword();
	}

	Param(std::string n, std::string default_val){
		name = n;
		val = default_val;

		set_definition_keyword();
	}

	/// If this param is a symbol, set the correct keyword that should be used to define it based on the front-end
	void set_definition_keyword(){
		if (f == f_qiskit){
			definition_keyword = "Parameter";
		} else if (f == f_pytket){
			definition_keyword = "Symbol";
		}
	}
};

typedef enum {
	no_circbox = 1,
	no_paulibox = 2,
	no_mult = 4,
	no_named_qubits = 8,
	no_bits = 16
} restriction;

typedef enum{
	rt_none,
	index,
	named
} resource_type;


extern std::vector<std::string> qiskit_opt_passes, cirq_target_gatesets, cirq_insert_strats, cirq_all_passes;

extern fs::path CIRCUITS_DIR;

extern frontend f;

#endif