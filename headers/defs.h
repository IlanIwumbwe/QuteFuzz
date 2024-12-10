#ifndef DEFS_H
#define DEFS_H

#define set_bit(ind) (1ULL << ind)  // return a 64 bit number

typedef unsigned char U4;
typedef unsigned long long ULL;
namespace fs = std::filesystem;

typedef enum {
	noop = set_bit(0),
	cy = set_bit(1),
	multiplexor = set_bit(2),
	circbox = set_bit(3),
	paulibox = set_bit(4),
	ry = set_bit(5),
	unitary_box = set_bit(6),
	cnx = set_bit(7),
	tk1 = set_bit(8),
	tk2 = set_bit(9),
	cx = set_bit(10),
	cz = set_bit(11),
	swap = set_bit(12),
	rx = set_bit(13),
	rz = set_bit(14),
	h = set_bit(15),
	x = set_bit(16),
	z = set_bit(17),
	y = set_bit(18),
	v = set_bit(19),
	s = set_bit(20),
	u1 = set_bit(21),
	u2 = set_bit(22),
	u3 = set_bit(23),
	cny = set_bit(24),
	cnz = set_bit(25),
	cnrx = set_bit(26),
	cnry = set_bit(27),
	cnrz = set_bit(28),
	xxphase = set_bit(29),
	yyphase = set_bit(30),
	zzphase = set_bit(31),
	sx = set_bit(32),
	u = set_bit(33),
	crx = set_bit(34),
	cry = set_bit(35),
	crz = set_bit(36),
	t = set_bit(37),
	cswap = set_bit(38),
	phasedxz = set_bit(39),
	phasedxpow = set_bit(40),
} gate_type;

// flags used to restrict pytket gatesets
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

typedef enum {
	f_pytket = 0,
	f_qiskit,
	f_cirq,
} frontend;

typedef enum {
	no_circbox = 1,
	no_paulibox = 2,
	no_mult = 4,
	no_named_qubits = 8,
	no_bits = 16
} restriction_flags;

typedef enum{
	rt_none,
	index,
	named
} resource_type;

typedef enum {
	subroutine,
	main_circ
} circuit_kind;

#endif