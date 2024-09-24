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
subcirc0.cx(qreg_1[0],qreg_0[0])
subcirc0.u(0,0,-0.407000, qreg_1[0])
subcirc0.cx(qreg_1[0],qreg_0[0])
subcirc0.u(0,0,-0.020000, qreg_1[0])
subcirc0.cx(qreg_1[0],qreg_0[0])
subcirc0.ry(0.414000, qreg_0[0])

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc1.add_register(qreg_0)
# Adding creg resources 
subcirc1.u(0,0,0.792000, qreg_0[1])
subcirc1.rx(0.965000, qreg_0[1])
subcirc1.ry(-0.173000, qreg_0[1])
subcirc1.u(0,0,-0.435000, qreg_0[0])
subcirc1.rx(0.162000, qreg_0[0])
subcirc1.cx(qreg_0[0],qreg_0[1])

subcirc2 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc2.add_register(qreg_0)
# Adding creg resources 
subcirc2.cx(qreg_0[0],qreg_0[1])
subcirc2.u(0,0,0.663000, qreg_0[1])
subcirc2.u(0,0,-0.699000, qreg_0[0])
subcirc2.u(0,0,0.436000, qreg_0[0])
subcirc2.ry(-0.628000, qreg_0[0])
subcirc2.ry(-0.995000, qreg_0[1])

subcirc3 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc3.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc3.add_register(qreg_1)
# Adding creg resources 
subcirc3.rx(0.252000, qreg_1[0])
subcirc3.u(0,0,-0.302000, qreg_0[0])
subcirc3.u(0,0,0.553000, qreg_0[0])
subcirc3.ry(0.239000, qreg_0[0])
subcirc3.ry(0.840000, qreg_1[0])
subcirc3.ry(0.994000, qreg_1[0])
subcirc3 = subcirc3.to_gate().control(2)

subcirc4 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc4.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc4.add_register(qreg_1)
# Adding creg resources 
subcirc4.rx(-0.231000, qreg_0[0])
subcirc4.ry(-0.467000, qreg_0[0])
subcirc4.ry(-0.434000, qreg_1[0])
subcirc4.ry(-0.833000, qreg_0[0])
subcirc4.cx(qreg_1[0],qreg_0[0])
subcirc4.u(0,0,-0.480000, qreg_0[0])
subcirc4 = subcirc4.to_gate().control(3)

main_circ = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
main_circ.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
main_circ.add_register(qreg_1)
qreg_2 = QuantumRegister(1)
main_circ.add_register(qreg_2)
qreg_3 = QuantumRegister(1)
main_circ.add_register(qreg_3)
# Adding creg resources 
creg_0 = ClassicalRegister(2)
main_circ.add_register(creg_0)
# Adding symbols 
param_0 = Parameter("param_0")
param_1 = Parameter("param_1")
param_2 = Parameter("param_2")

main_circ.append(subcirc0,[qreg_2[0],qreg_3[0]])
main_circ.measure(qreg_3[0], creg_0[0])
with main_circ.if_test((creg_0[0],0)):
	main_circ.append(subcirc2,[qreg_3[0],qreg_1[0]])
main_circ.append(subcirc3,[qreg_2[0],qreg_1[0],qreg_0[0],qreg_3[0]])
main_circ.cx(qreg_1[0],qreg_2[0])
main_circ.cx(qreg_2[0],qreg_1[0])
bindings = {}
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
main_circ.measure_active()
run_on_simulator(main_circ, 9)
