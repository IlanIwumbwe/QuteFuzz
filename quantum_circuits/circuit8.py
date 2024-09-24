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
subcirc0.cz(qreg_0[1],qreg_0[0])
subcirc0.rz(-0.117000, qreg_0[0])
subcirc0.rz(0.814000, qreg_0[0])
subcirc0.x(qreg_0[1])
subcirc0.x(qreg_0[0])

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc1.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc1.add_register(qreg_1)
# Adding creg resources 
subcirc1.x(qreg_0[0])
subcirc1.u(-0.692000,0.315000,0.478000, qreg_0[0])
subcirc1.u(0.032000,-0.761000,-0.568000, qreg_0[0])
subcirc1.x(qreg_0[0])
subcirc1.rz(-0.788000, qreg_0[0])
subcirc1 = subcirc1.to_gate().control(1)

subcirc2 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc2.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc2.add_register(qreg_1)
# Adding creg resources 
subcirc2.x(qreg_1[0])
subcirc2.cz(qreg_0[0],qreg_1[0])
subcirc2.cz(qreg_0[0],qreg_1[0])
subcirc2.rz(-0.613000, qreg_0[0])
subcirc2.x(qreg_0[0])

subcirc3 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc3.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc3.add_register(qreg_1)
# Adding creg resources 
subcirc3.rz(-0.156000, qreg_0[0])
subcirc3.cz(qreg_1[0],qreg_0[0])
subcirc3.rz(0.386000, qreg_0[0])
subcirc3.x(qreg_1[0])
subcirc3.rz(0.792000, qreg_1[0])

main_circ = QuantumCircuit(2)
# Adding qregs 
qreg_0 = QuantumRegister(2)
main_circ.add_register(qreg_0)
qreg_2 = QuantumRegister(2)
main_circ.add_register(qreg_2)
# Adding creg resources 
creg_0 = ClassicalRegister(1)
main_circ.add_register(creg_0)
creg_1 = ClassicalRegister(1)
main_circ.add_register(creg_1)
# Adding symbols 
param_0 = Parameter("param_0")
param_1 = Parameter("param_1")
param_2 = Parameter("param_2")
param_3 = Parameter("param_3")

main_circ.measure(1, creg_1[0])
with main_circ.if_test((creg_1[0],0)):
	main_circ.measure(qreg_0[0], creg_1[0])
	with main_circ.switch(creg_1[0]) as case_2:
		with case_2(0):
			main_circ.measure(1, creg_1[0])
			with main_circ.switch(creg_1[0]) as case_1:
				with case_1(0):
					main_circ.u(param_0,param_2,param_1, qreg_0[1])
					main_circ.cz(1,qreg_2[1])
					main_circ.append(subcirc2,[1,qreg_2[0]])
				with case_1(1):
					main_circ.cz(qreg_0[0],qreg_0[1])
					main_circ.append(subcirc3,[qreg_0[1],0])
		with case_2(1):
			main_circ.measure(0, creg_1[0])
			with main_circ.if_test((creg_1[0],0)) as else_1:
				main_circ.append(subcirc1,[qreg_2[1],0,qreg_0[0]])
			with else_1:
				main_circ.append(subcirc0,[qreg_0[1],0])
main_circ.measure(qreg_0[0], creg_0[0])
with main_circ.if_test((creg_0[0],0)) as else_3:
	main_circ.measure(qreg_0[0], creg_1[0])
	with main_circ.switch(creg_1[0]) as case_2:
		with case_2(0):
			main_circ.measure(qreg_0[1], creg_1[0])
			with main_circ.switch(creg_1[0]) as case_1:
				with case_1(0):
					main_circ.rz(param_0, qreg_2[0])
					main_circ.append(subcirc2,[qreg_0[0],qreg_0[1]])
				with case_1(1):
					main_circ.u(param_2,-0.873000,param_2, qreg_2[0])
					main_circ.cz(qreg_0[1],qreg_0[0])
					main_circ.append(subcirc3,[0,qreg_2[1]])
		with case_2(1):
			main_circ.rz(param_3, qreg_0[1])
			main_circ.measure(qreg_0[0], creg_1[0])
			with main_circ.switch(creg_1[0]) as case_1:
				with case_1(0):
					main_circ.rz(param_1, 1)
					main_circ.cz(0,qreg_0[1])
					main_circ.cz(qreg_0[0],0)
					main_circ.rz(-0.192000, 1)
				with case_1(1):
					main_circ.rz(param_2, qreg_0[0])
					main_circ.rz(0.783000, qreg_2[0])
					main_circ.append(subcirc2,[qreg_0[0],qreg_0[1]])
with else_3:
	main_circ.cz(qreg_2[1],0)
	main_circ.measure(qreg_0[1], creg_1[0])
	with main_circ.if_test((creg_1[0],0)):
		main_circ.measure(qreg_0[1], creg_1[0])
		with main_circ.switch(creg_1[0]) as case_1:
			with case_1(0):
				main_circ.cz(qreg_2[1],qreg_2[0])
				main_circ.cz(qreg_2[1],qreg_0[0])
				main_circ.cz(0,qreg_2[1])
				main_circ.x(0)
			with case_1(1):
				main_circ.rz(0.579000, 1)
				main_circ.u(0.736000,0.230000,0.413000, qreg_0[0])
				main_circ.append(subcirc1,[qreg_2[1],1,qreg_0[0]])
main_circ.measure(qreg_0[0], creg_1[0])
with main_circ.if_test((creg_1[0],0)):
	main_circ.measure(0, creg_0[0])
	with main_circ.switch(creg_0[0]) as case_2:
		with case_2(0):
			main_circ.measure(qreg_2[0], creg_1[0])
			with main_circ.if_test((creg_1[0],0)) as else_1:
				main_circ.rz(-0.280000, qreg_0[1])
				main_circ.x(qreg_2[0])
			with else_1:
				main_circ.u(-0.892000,param_1,0.088000, 1)
			main_circ.barrier(qreg_2[1])
		with case_2(1):
			main_circ.measure(qreg_0[0], creg_1[0])
			with main_circ.if_test((creg_1[0],0)):
				main_circ.barrier(qreg_0[1])
			main_circ.measure(qreg_0[1], creg_0[0])
			with main_circ.if_test((creg_0[0],0)) as else_1:
				main_circ.id(1)
			with else_1:
				main_circ.barrier(0)
			main_circ.barrier(qreg_0[1])
	main_circ.barrier(qreg_2[1])
bindings = {param_0: -0.165000, param_1: 0.759000, param_2: -0.865000, param_3: 0.938000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
main_circ.measure_active()
run_on_simulator(main_circ, 8)
