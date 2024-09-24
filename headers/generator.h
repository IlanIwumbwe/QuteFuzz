#ifndef GENERATOR_H
#define GENERATOR_H

#include <vector>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <optional>
#include "../headers/circuit.h"

namespace pytket {

	void write_imports(std::ofstream& stream, unsigned int restriction);

	void add_resources(std::ofstream& stream, circuit_info& info);

	void write_circuit(std::ofstream& stream, circuit_info& info);

	void write_circboxes(std::ofstream& stream, circuit_info& info);

	void write_multiplexor(std::ofstream& stream, circuit_info& info);

	void apply_gates(std::ofstream& stream, circuit_info& info);

	void write_pauli_exp(std::ofstream& stream, circuit_info& info);

	void generate_circuits(int n);
};

namespace qiskit {

	void write_imports(std::ofstream& stream);

	void add_resources(std::ofstream& stream, circuit_info& info);

	void write_circuit(std::ofstream& stream, circuit_info& info);

	void write_circboxes(std::ofstream& stream, circuit_info& info);

	int write_if(std::ofstream& stream, circuit_info& info, int depth);

	int write_if_else(std::ofstream& stream, circuit_info& info, int depth);

	int write_switch(std::ofstream& stream, circuit_info& info, int depth);

	int apply_gates(std::ofstream& stream, circuit_info& info, int gates_to_apply, int nest_depth);

	void add_measure(std::ofstream& stream, circuit_info& info, Resource* br);

	void add_barrier(std::ofstream& stream, circuit_info& info);

	void add_noop(std::ofstream& stream, circuit_info& info);

	void generate_circuits(int n);
};

namespace cirq {
	extern int cirq_measures;

	void write_imports(std::ofstream& stream, circuit_info& info);

	void write_circuit(std::ofstream& stream, circuit_info& info);

	void write_circboxes(std::ofstream& stream, circuit_info& info);

	void add_measure(std::ofstream& stream, circuit_info& info);

	void add_resources(std::ofstream& stream, circuit_info& info);

	void apply_gates(std::ofstream& stream, circuit_info& info);

	int apply_gate(std::ofstream& stream, circuit_info& info, Gate& g);

	void write_qubit_replacement(std::ofstream& stream, circuit_info& info, Gate& g);

	void transfer_concurrencies(circuit_info& info, Gate& g);

	void generate_circuits(int n);
};

bool get_any_qubits(circuit_info& info, int n, std::vector<Resource>& chosen_resources);

bool get_n_similar_qubits(circuit_info& info, int n, std::vector<Resource>& chosen_resources);

void get_particular_qubits(circuit_info& info, int n, std::vector<Resource>& chosen_resources, resource_type rt);

int apply_gate(std::ofstream& stream, circuit_info& info, Gate& g, bool (*resource_getter)(circuit_info&, int, std::vector<Resource>&));

void write_resources(std::ofstream& stream, Gate& gate);

void write_args(std::ofstream& stream, circuit_info& info, Gate& gate);

void write_gate(std::ofstream& stream, circuit_info& info, Gate& g, std::string special_options = "",  std::string special_modifications = "");

void generate(int n);

void add_symbols(std::ofstream& stream, circuit_info& info);

#endif
