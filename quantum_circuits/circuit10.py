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
subcirc0.cz(qreg_1[0],qreg_0[0])
subcirc0.cz(qreg_1[0],qreg_0[0])
subcirc0.cz(qreg_0[0],qreg_1[0])
subcirc0.rz(0.223000, qreg_1[0])
subcirc0.cz(qreg_1[0],qreg_0[0])
subcirc0.cy(qreg_1[0],qreg_0[0])

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc1.add_register(qreg_0)
# Adding creg resources 
subcirc1.cy(qreg_0[1],qreg_0[0])
subcirc1.cz(qreg_0[1],qreg_0[0])
subcirc1.y(qreg_0[0])
subcirc1.rz(-0.921000, qreg_0[0])
subcirc1.rz(-0.076000, qreg_0[1])
subcirc1.cy(qreg_0[1],qreg_0[0])

subcirc2 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc2.add_register(qreg_0)
# Adding creg resources 
subcirc2.cz(qreg_0[1],qreg_0[0])
subcirc2.y(qreg_0[1])
subcirc2.rz(-0.322000, qreg_0[1])
subcirc2.y(qreg_0[1])
subcirc2.y(qreg_0[0])
subcirc2.cz(qreg_0[1],qreg_0[0])
subcirc2 = subcirc2.to_gate().control(3)

main_circ = QuantumCircuit(1)
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
param_4 = Parameter("param_4")
param_5 = Parameter("param_5")

main_circ.cz(qreg_0[1],qreg_2[1])
main_circ.rz(-0.177000, 0)
main_circ.measure(qreg_2[0], creg_1[0])
with main_circ.switch(creg_1[0]) as case_3:
	with case_3(0):
		main_circ.measure(0, creg_0[0])
		with main_circ.switch(creg_0[0]) as case_2:
			with case_2(0):
				main_circ.measure(qreg_0[0], creg_1[0])
				with main_circ.switch(creg_1[0]) as case_1:
					with case_1(0):
						main_circ.rz(-0.545000, qreg_2[1])
						main_circ.append(subcirc0,[qreg_2[1],qreg_0[1]])
					with case_1(1):
						main_circ.append(subcirc1,[qreg_2[1],0])
			with case_2(1):
				main_circ.measure(qreg_0[1], creg_1[0])
				with main_circ.if_test((creg_1[0],0)):
					main_circ.append(subcirc1,[0,qreg_2[0]])
	with case_3(1):
		main_circ.measure(0, creg_0[0])
		with main_circ.switch(creg_0[0]) as case_2:
			with case_2(0):
				main_circ.measure(0, creg_0[0])
				with main_circ.if_test((creg_0[0],0)):
					main_circ.y(qreg_2[0])
					main_circ.append(subcirc1,[qreg_2[0],0])
			with case_2(1):
				main_circ.measure(qreg_2[0], creg_1[0])
				with main_circ.switch(creg_1[0]) as case_1:
					with case_1(0):
						main_circ.cz(0,qreg_2[0])
						main_circ.append(subcirc1,[qreg_0[0],qreg_2[1]])
					with case_1(1):
						main_circ.append(subcirc1,[qreg_2[1],qreg_2[0]])
main_circ.measure(qreg_2[1], creg_1[0])
with main_circ.if_test((creg_1[0],0)) as else_3:
	main_circ.rz(param_3, qreg_2[1])
	main_circ.measure(qreg_0[1], creg_0[0])
	with main_circ.if_test((creg_0[0],0)):
		main_circ.measure(qreg_2[1], creg_1[0])
		with main_circ.switch(creg_1[0]) as case_1:
			with case_1(0):
				main_circ.y(qreg_0[1])
				main_circ.rz(-0.741000, qreg_0[1])
				main_circ.y(0)
				main_circ.append(subcirc2,[qreg_0[0],0,qreg_2[1],qreg_0[1],qreg_2[0]])
			with case_1(1):
				main_circ.append(subcirc1,[0,qreg_2[1]])
with else_3:
	main_circ.measure(qreg_0[1], creg_1[0])
	with main_circ.switch(creg_1[0]) as case_2:
		with case_2(0):
			main_circ.measure(qreg_0[1], creg_1[0])
			with main_circ.switch(creg_1[0]) as case_1:
				with case_1(0):
					main_circ.barrier(qreg_2[0])
				with case_1(1):
					main_circ.id(qreg_2[1])
			main_circ.measure(qreg_2[1], creg_0[0])
			with main_circ.switch(creg_0[0]) as case_1:
				with case_1(0):
					main_circ.id(qreg_2[0])
				with case_1(1):
					main_circ.id(qreg_2[1])
			main_circ.measure(qreg_2[0], creg_0[0])
			with main_circ.switch(creg_0[0]) as case_1:
				with case_1(0):
					main_circ.barrier(qreg_0[1])
				with case_1(1):
					main_circ.barrier(qreg_0[0])
			main_circ.measure(qreg_2[1], creg_1[0])
			with main_circ.if_test((creg_1[0],0)) as else_1:
				main_circ.barrier(qreg_0[0])
			with else_1:
				main_circ.barrier(qreg_0[0])
			main_circ.measure(0, creg_1[0])
			with main_circ.if_test((creg_1[0],0)) as else_1:
				main_circ.barrier(qreg_2[1])
			with else_1:
				main_circ.id(qreg_0[1])
			main_circ.measure(qreg_0[0], creg_1[0])
			with main_circ.if_test((creg_1[0],0)):
				main_circ.id(qreg_2[1])
			main_circ.id(qreg_0[0])
		with case_2(1):
			main_circ.measure(qreg_0[0], creg_0[0])
			with main_circ.switch(creg_0[0]) as case_1:
				with case_1(0):
					main_circ.barrier(0)
				with case_1(1):
					main_circ.barrier(qreg_0[1])
			main_circ.measure(qreg_2[0], creg_0[0])
			with main_circ.if_test((creg_0[0],0)):
				main_circ.id(qreg_2[1])
			main_circ.id(0)
	main_circ.measure(qreg_0[1], creg_0[0])
	with main_circ.switch(creg_0[0]) as case_2:
		with case_2(0):
			main_circ.measure(qreg_0[1], creg_0[0])
			with main_circ.if_test((creg_0[0],0)):
				main_circ.barrier(qreg_0[0])
			main_circ.measure(qreg_2[1], creg_1[0])
			with main_circ.if_test((creg_1[0],0)) as else_1:
				main_circ.id(qreg_2[1])
			with else_1:
				main_circ.barrier(0)
			main_circ.measure(qreg_2[1], creg_1[0])
			with main_circ.if_test((creg_1[0],0)):
				main_circ.barrier(qreg_0[0])
			main_circ.measure(qreg_2[0], creg_0[0])
			with main_circ.if_test((creg_0[0],0)) as else_1:
				main_circ.barrier(qreg_0[0])
			with else_1:
				main_circ.barrier(0)
			main_circ.measure(qreg_0[0], creg_1[0])
			with main_circ.switch(creg_1[0]) as case_1:
				with case_1(0):
					main_circ.barrier(qreg_0[1])
				with case_1(1):
					main_circ.id(qreg_2[0])
			main_circ.measure(0, creg_0[0])
			with main_circ.switch(creg_0[0]) as case_1:
				with case_1(0):
					main_circ.id(qreg_2[0])
				with case_1(1):
					main_circ.id(qreg_0[0])
			main_circ.measure(qreg_0[1], creg_1[0])
			with main_circ.if_test((creg_1[0],0)) as else_1:
				main_circ.barrier(0)
			with else_1:
				main_circ.barrier(qreg_2[1])
			main_circ.measure(qreg_2[1], creg_0[0])
			with main_circ.switch(creg_0[0]) as case_1:
				with case_1(0):
					main_circ.barrier(qreg_2[1])
				with case_1(1):
					main_circ.id(qreg_2[0])
			main_circ.barrier(qreg_0[1])
		with case_2(1):
			main_circ.barrier(qreg_0[0])
	main_circ.measure(qreg_2[1], creg_1[0])
	with main_circ.if_test((creg_1[0],0)):
		main_circ.measure(0, creg_0[0])
		with main_circ.if_test((creg_0[0],0)):
			main_circ.barrier(0)
		main_circ.measure(qreg_2[0], creg_0[0])
		with main_circ.if_test((creg_0[0],0)) as else_1:
			main_circ.barrier(qreg_2[1])
		with else_1:
			main_circ.id(qreg_2[1])
		main_circ.id(qreg_2[0])
	main_circ.measure(qreg_0[0], creg_0[0])
	with main_circ.if_test((creg_0[0],0)):
		main_circ.id(qreg_2[0])
	main_circ.measure(qreg_0[0], creg_0[0])
	with main_circ.if_test((creg_0[0],0)):
		main_circ.measure(qreg_0[1], creg_1[0])
		with main_circ.switch(creg_1[0]) as case_1:
			with case_1(0):
				main_circ.id(qreg_2[1])
			with case_1(1):
				main_circ.barrier(qreg_2[0])
		main_circ.measure(qreg_2[1], creg_1[0])
		with main_circ.if_test((creg_1[0],0)) as else_1:
			main_circ.id(qreg_2[1])
		with else_1:
			main_circ.id(qreg_0[0])
		main_circ.id(qreg_0[0])
	main_circ.barrier(qreg_0[1])
bindings = {param_3: -0.186000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
main_circ.measure_active()
run_on_simulator(main_circ, 10)
