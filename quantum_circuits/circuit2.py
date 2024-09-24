from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter, ParameterVector
from helpers.qiskit_helpers import compare_statevectors, run_on_simulator, run_routing_simulation
from pathlib import Path
from math import pi

subcirc0 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc0.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc0.add_register(qreg_1)
# Adding creg resources 
subcirc0.rz(0.964000, qreg_0[0])
subcirc0.cy(qreg_0[0],qreg_1[0])
subcirc0.cx(qreg_0[0],qreg_1[0])
subcirc0.rz(-0.156000, qreg_0[0])
subcirc0.cx(qreg_1[0],qreg_0[0])
subcirc0.rx(-0.457000, qreg_1[0])
subcirc0 = subcirc0.to_gate().control(1)

main_circ = QuantumCircuit(4)
# Adding qregs 
qreg_0 = QuantumRegister(1)
main_circ.add_register(qreg_0)
# Adding creg resources 
creg_0 = ClassicalRegister(1)
main_circ.add_register(creg_0)
creg_1 = ClassicalRegister(1)
main_circ.add_register(creg_1)
# Adding symbols 
param_0 = Parameter("param_0")

main_circ.measure(1, creg_0[0])
with main_circ.switch(creg_0[0]) as case_1:
	with case_1(0):
		main_circ.rx(param_0, 3)
		main_circ.append(subcirc0,[1,3,qreg_0[0]])
	with case_1(1):
		main_circ.cx(1,2)
		main_circ.append(subcirc0,[2,0,qreg_0[0]])
main_circ.measure(0, creg_0[0])
with main_circ.if_test((creg_0[0],0)):
	main_circ.append(subcirc0,[qreg_0[0],1,0])
main_circ.measure(qreg_0[0], creg_0[0])
with main_circ.if_test((creg_0[0],0)):
	main_circ.cx(1,3)
	main_circ.rz(-0.916000, 1)
	main_circ.rz(0.845000, 3)
	main_circ.cx(0,qreg_0[0])
main_circ.rx(param_0, 3)
main_circ.rz(0.191000, 0)
main_circ.measure(qreg_0[0], creg_0[0])
with main_circ.if_test((creg_0[0],0)) as else_1:
	main_circ.cx(qreg_0[0],1)
with else_1:
	main_circ.rx(param_0, 3)
	main_circ.cx(2,3)
main_circ.measure(3, creg_1[0])
with main_circ.switch(creg_1[0]) as case_1:
	with case_1(0):
		main_circ.cx(2,1)
		main_circ.cx(1,0)
		main_circ.cy(3,2)
		main_circ.rz(param_0, 1)
	with case_1(1):
		main_circ.cx(qreg_0[0],1)
		main_circ.rx(param_0, 0)
		main_circ.rz(param_0, 2)
		main_circ.rz(param_0, 1)
main_circ.measure(2, creg_1[0])
with main_circ.switch(creg_1[0]) as case_1:
	with case_1(0):
		main_circ.rz(param_0, 3)
		main_circ.append(subcirc0,[qreg_0[0],0,1])
	with case_1(1):
		main_circ.cx(3,1)
		main_circ.rx(0.576000, 2)
		main_circ.append(subcirc0,[3,2,qreg_0[0]])
main_circ.append(subcirc0,[1,0,3])
main_circ.measure(1, creg_0[0])
with main_circ.switch(creg_0[0]) as case_1:
	with case_1(0):
		main_circ.rx(-0.358000, 1)
		main_circ.cx(2,0)
		main_circ.cy(0,3)
		main_circ.barrier(3)
	with case_1(1):
		main_circ.cx(0,qreg_0[0])
		main_circ.cy(2,0)
		main_circ.id(2)
bindings = {param_0: -0.533000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
main_circ.measure_active()
run_on_simulator(main_circ, 2)
