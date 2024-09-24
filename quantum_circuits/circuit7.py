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
subcirc0.rx(0.188000, qreg_0[0])
subcirc0.u(pi/2,0.839000,0.910000, qreg_0[1])
subcirc0.rx(0.223000, qreg_0[0])
subcirc0.u(pi/2,-0.159000,-0.620000, qreg_0[0])
subcirc0.rx(0.020000, qreg_0[1])
subcirc0.z(qreg_0[0])
subcirc0 = subcirc0.to_gate().control(2)

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc1.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc1.add_register(qreg_1)
# Adding creg resources 
subcirc1.rz(0.641000, qreg_0[0])
subcirc1.rx(0.501000, qreg_0[0])
subcirc1.rx(0.696000, qreg_0[0])
subcirc1.rz(0.384000, qreg_0[0])
subcirc1.rx(-0.981000, qreg_0[0])
subcirc1.z(qreg_1[0])
subcirc1 = subcirc1.to_gate().control(1)

subcirc2 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc2.add_register(qreg_0)
# Adding creg resources 
subcirc2.u(pi/2,0.477000,-0.645000, qreg_0[0])
subcirc2.rx(-0.015000, qreg_0[0])
subcirc2.z(qreg_0[1])
subcirc2.rx(0.203000, qreg_0[1])
subcirc2.rx(0.239000, qreg_0[0])
subcirc2.u(pi/2,0.248000,-0.722000, qreg_0[1])

main_circ = QuantumCircuit(1)
# Adding qregs 
qreg_0 = QuantumRegister(3)
main_circ.add_register(qreg_0)
qreg_3 = QuantumRegister(1)
main_circ.add_register(qreg_3)
# Adding creg resources 
creg_0 = ClassicalRegister(2)
main_circ.add_register(creg_0)
# Adding symbols 
param_0 = Parameter("param_0")
param_1 = Parameter("param_1")

main_circ.measure(qreg_0[0], creg_0[0])
with main_circ.switch(creg_0[0]) as case_3:
	with case_3(0):
		main_circ.z(qreg_3[0])
		main_circ.measure(qreg_3[0], creg_0[1])
		with main_circ.if_test((creg_0[1],0)) as else_2:
			main_circ.measure(0, creg_0[1])
			with main_circ.switch(creg_0[1]) as case_1:
				with case_1(0):
					main_circ.append(subcirc2,[0,qreg_0[2]])
				with case_1(1):
					main_circ.u(param_1,0.570000,param_1, 0)
					main_circ.rz(0.832000, qreg_3[0])
					main_circ.append(subcirc1,[qreg_0[1],qreg_0[2],qreg_3[0]])
		with else_2:
			main_circ.measure(qreg_0[2], creg_0[1])
			with main_circ.if_test((creg_0[1],0)):
				main_circ.append(subcirc0,[0,qreg_0[0],qreg_3[0],qreg_0[2]])
	with case_3(1):
		main_circ.measure(qreg_0[1], creg_0[0])
		with main_circ.if_test((creg_0[0],0)):
			main_circ.measure(qreg_0[1], creg_0[0])
			with main_circ.if_test((creg_0[0],0)):
				main_circ.barrier(qreg_0[0])
			main_circ.measure(qreg_0[2], creg_0[0])
			with main_circ.if_test((creg_0[0],0)):
				main_circ.id(qreg_0[1])
			main_circ.measure(0, creg_0[1])
			with main_circ.if_test((creg_0[1],0)):
				main_circ.barrier(qreg_0[2])
			main_circ.measure(qreg_0[2], creg_0[0])
			with main_circ.if_test((creg_0[0],0)) as else_1:
				main_circ.rx(-0.696000, 0)
				main_circ.id(qreg_0[1])
			with else_1:
				main_circ.id(qreg_3[0])
			main_circ.measure(qreg_0[1], creg_0[0])
			with main_circ.switch(creg_0[0]) as case_1:
				with case_1(0):
					main_circ.rx(param_1, qreg_0[2])
					main_circ.u(pi/2,param_1,0.311000, qreg_0[0])
					main_circ.id(0)
				with case_1(1):
					main_circ.rz(0.886000, 0)
					main_circ.rz(param_1, 0)
					main_circ.barrier(qreg_0[0])
bindings = {param_1: -0.364000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
main_circ.measure_active()
run_on_simulator(main_circ, 7)
