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
subcirc0.z(qreg_0[0])
subcirc0.x(qreg_0[0])
subcirc0.u(0,0,-0.786000, qreg_0[0])
subcirc0.ry(-0.864000, qreg_1[0])
subcirc0.z(qreg_0[0])
subcirc0.ry(0.413000, qreg_0[0])

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc1.add_register(qreg_0)
# Adding creg resources 
subcirc1.ry(-0.207000, qreg_0[1])
subcirc1.ry(0.746000, qreg_0[0])
subcirc1.u(0,0,-0.673000, qreg_0[0])
subcirc1.u(0,0,0.285000, qreg_0[0])
subcirc1.u(0,0,-0.446000, qreg_0[1])
subcirc1.z(qreg_0[0])

subcirc2 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc2.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc2.add_register(qreg_1)
# Adding creg resources 
subcirc2.x(qreg_1[0])
subcirc2.z(qreg_1[0])
subcirc2.ry(-0.254000, qreg_0[0])
subcirc2.x(qreg_1[0])
subcirc2.z(qreg_0[0])
subcirc2.ry(0.580000, qreg_1[0])

subcirc3 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc3.add_register(qreg_0)
# Adding creg resources 
subcirc3.z(qreg_0[0])
subcirc3.x(qreg_0[1])
subcirc3.u(0,0,-0.507000, qreg_0[0])
subcirc3.x(qreg_0[1])
subcirc3.u(0,0,0.568000, qreg_0[0])
subcirc3.x(qreg_0[1])

subcirc4 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc4.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc4.add_register(qreg_1)
# Adding creg resources 
subcirc4.x(qreg_0[0])
subcirc4.ry(0.947000, qreg_0[0])
subcirc4.x(qreg_0[0])
subcirc4.z(qreg_0[0])
subcirc4.x(qreg_0[0])
subcirc4.u(0,0,-0.161000, qreg_0[0])
subcirc4 = subcirc4.to_gate().control(1)

main_circ = QuantumCircuit(4)
# Adding qregs 
qreg_0 = QuantumRegister(2)
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
param_3 = Parameter("param_3")
param_4 = Parameter("param_4")
param_5 = Parameter("param_5")
param_6 = Parameter("param_6")

main_circ.append(subcirc4,[3,qreg_0[1],1])
main_circ.x(3)
main_circ.x(1)
main_circ.x(qreg_0[0])
main_circ.append(subcirc2,[2,0])
main_circ.z(2)
main_circ.append(subcirc3,[qreg_0[0],3])
main_circ.append(subcirc3,[qreg_0[1],0])
main_circ.append(subcirc0,[qreg_0[1],qreg_0[0]])
main_circ.append(subcirc1,[0,2])
main_circ.z(0)
main_circ.ry(param_0, 2)
main_circ.append(subcirc4,[qreg_0[1],qreg_0[0],3])
main_circ.append(subcirc0,[qreg_0[0],2])
main_circ.append(subcirc3,[0,qreg_0[0]])
main_circ.x(3)
main_circ.u(param_3,0,0.497000, 0)
main_circ.u(param_4,param_0,param_1, 2)
main_circ.x(0)
bindings = {param_0: 0.950000, param_1: -0.790000, param_3: -0.067000, param_4: -0.804000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
compare_statevectors(main_circ, "Optimize1qGates")
