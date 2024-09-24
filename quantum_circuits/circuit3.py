from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter, ParameterVector
from helpers.qiskit_helpers import compare_statevectors, run_on_simulator, run_routing_simulation
from pathlib import Path
from math import pi

subcirc0 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc0.add_register(qreg_0)
# Adding creg resources 
subcirc0.ry(-0.684000, qreg_0[0])
subcirc0.x(qreg_0[0])
subcirc0.x(qreg_0[0])
subcirc0.cz(qreg_0[0],qreg_0[1])
subcirc0 = subcirc0.to_gate().control(2)

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc1.add_register(qreg_0)
# Adding creg resources 
subcirc1.cz(qreg_0[1],qreg_0[0])
subcirc1.u(pi/2,0.496000,-0.984000, qreg_0[0])
subcirc1.x(qreg_0[1])
subcirc1.ry(0.554000, qreg_0[0])
subcirc1 = subcirc1.to_gate().control(2)

main_circ = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(4)
main_circ.add_register(qreg_0)
# Adding creg resources 
creg_0 = ClassicalRegister(1)
main_circ.add_register(creg_0)
creg_1 = ClassicalRegister(1)
main_circ.add_register(creg_1)
# Adding symbols 
param_0 = Parameter("param_0")
param_1 = Parameter("param_1")
param_2 = Parameter("param_2")

main_circ.measure(qreg_0[3], creg_1[0])
with main_circ.switch(creg_1[0]) as case_1:
	with case_1(0):
		main_circ.append(subcirc0,[qreg_0[0],qreg_0[2],qreg_0[1],qreg_0[3]])
	with case_1(1):
		main_circ.append(subcirc1,[qreg_0[1],qreg_0[2],qreg_0[0],qreg_0[3]])
main_circ.measure(qreg_0[3], creg_0[0])
with main_circ.switch(creg_0[0]) as case_1:
	with case_1(0):
		main_circ.ry(param_1, qreg_0[1])
		main_circ.cz(qreg_0[1],qreg_0[3])
		main_circ.x(qreg_0[0])
		main_circ.append(subcirc0,[qreg_0[3],qreg_0[0],qreg_0[2],qreg_0[1]])
	with case_1(1):
		main_circ.append(subcirc0,[qreg_0[1],qreg_0[2],qreg_0[3],qreg_0[0]])
main_circ.measure(qreg_0[3], creg_0[0])
with main_circ.if_test((creg_0[0],0)) as else_1:
	main_circ.cz(qreg_0[1],qreg_0[0])
with else_1:
	main_circ.cz(qreg_0[0],qreg_0[3])
main_circ.measure(qreg_0[2], creg_1[0])
with main_circ.if_test((creg_1[0],0)) as else_1:
	main_circ.append(subcirc0,[qreg_0[2],qreg_0[0],qreg_0[3],qreg_0[1]])
with else_1:
	main_circ.u(pi/2,param_0,0.113000, qreg_0[1])
main_circ.measure(qreg_0[2], creg_0[0])
with main_circ.if_test((creg_0[0],0)) as else_1:
	main_circ.u(param_2,0.974000,param_2, qreg_0[2])
	main_circ.cz(qreg_0[0],qreg_0[2])
with else_1:
	main_circ.x(qreg_0[0])
	main_circ.u(param_0,-0.378000,0.715000, qreg_0[1])
	main_circ.ry(-0.023000, qreg_0[2])
main_circ.measure(qreg_0[1], creg_1[0])
with main_circ.switch(creg_1[0]) as case_1:
	with case_1(0):
		main_circ.ry(param_2, qreg_0[3])
		main_circ.ry(param_0, qreg_0[0])
		main_circ.ry(param_0, qreg_0[3])
		main_circ.append(subcirc1,[qreg_0[3],qreg_0[2],qreg_0[1],qreg_0[0]])
	with case_1(1):
		main_circ.cz(qreg_0[2],qreg_0[0])
		main_circ.x(qreg_0[1])
		main_circ.u(pi/2,param_2,-0.223000, qreg_0[1])
		main_circ.ry(param_0, qreg_0[2])
main_circ.cz(qreg_0[2],qreg_0[1])
main_circ.cz(qreg_0[1],qreg_0[0])
main_circ.measure(qreg_0[0], creg_1[0])
with main_circ.if_test((creg_1[0],0)) as else_1:
	main_circ.cz(qreg_0[3],qreg_0[0])
	main_circ.cz(qreg_0[2],qreg_0[3])
with else_1:
	main_circ.cz(qreg_0[3],qreg_0[2])
main_circ.measure(qreg_0[3], creg_0[0])
with main_circ.if_test((creg_0[0],0)):
	main_circ.cz(qreg_0[2],qreg_0[1])
	main_circ.ry(0.041000, qreg_0[2])
main_circ.measure(qreg_0[1], creg_0[0])
with main_circ.if_test((creg_0[0],0)) as else_1:
	main_circ.cz(qreg_0[0],qreg_0[3])
	main_circ.u(param_0,0.542000,param_1, qreg_0[1])
	main_circ.cz(qreg_0[1],qreg_0[3])
with else_1:
	main_circ.append(subcirc0,[qreg_0[3],qreg_0[0],qreg_0[1],qreg_0[2]])
main_circ.measure(qreg_0[2], creg_1[0])
with main_circ.switch(creg_1[0]) as case_1:
	with case_1(0):
		main_circ.barrier(qreg_0[2])
	with case_1(1):
		main_circ.cz(qreg_0[1],qreg_0[2])
		main_circ.x(qreg_0[2])
		main_circ.cz(qreg_0[1],qreg_0[0])
		main_circ.barrier(qreg_0[2])
bindings = {param_0: 0.471000, param_1: 0.365000, param_2: -0.285000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
main_circ.measure_active()
run_on_simulator(main_circ, 3)
