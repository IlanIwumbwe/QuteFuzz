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
subcirc0.s(qreg_1[0])
subcirc0.h(qreg_0[0])
subcirc0.cy(qreg_0[0],qreg_1[0])
subcirc0.u(-0.735000,-0.994000,-0.439000, qreg_0[0])
subcirc0.u(-0.696000,0.998000,-0.242000, qreg_0[0])

subcirc1 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc1.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc1.add_register(qreg_1)
# Adding creg resources 
subcirc1.s(qreg_0[0])
subcirc1.s(qreg_0[0])
subcirc1.u(-0.994000,0.527000,-0.410000, qreg_0[0])
subcirc1.s(qreg_0[0])
subcirc1.h(qreg_0[0])
subcirc1 = subcirc1.to_gate().control(1)

subcirc2 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
subcirc2.add_register(qreg_0)
# Adding creg resources 
subcirc2.u(0.224000,-0.409000,-0.802000, qreg_0[1])
subcirc2.u(0.508000,-0.215000,0.141000, qreg_0[1])
subcirc2.u(0.140000,0.374000,-0.805000, qreg_0[1])
subcirc2.s(qreg_0[0])
subcirc2.u(0.298000,0.291000,0.136000, qreg_0[0])

subcirc3 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc3.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc3.add_register(qreg_1)
# Adding creg resources 
subcirc3.s(qreg_0[0])
subcirc3.u(-0.136000,-0.997000,0.253000, qreg_0[0])
subcirc3.u(0.983000,-0.172000,0.313000, qreg_0[0])
subcirc3.s(qreg_1[0])
subcirc3.cy(qreg_1[0],qreg_0[0])
subcirc3 = subcirc3.to_gate().control(3)

subcirc4 = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(1)
subcirc4.add_register(qreg_0)
qreg_1 = QuantumRegister(1)
subcirc4.add_register(qreg_1)
# Adding creg resources 
subcirc4.h(qreg_0[0])
subcirc4.u(-0.561000,-0.825000,0.780000, qreg_1[0])
subcirc4.s(qreg_0[0])
subcirc4.u(-0.441000,-0.306000,-0.188000, qreg_0[0])
subcirc4.h(qreg_1[0])

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
param_1 = Parameter("param_1")
param_2 = Parameter("param_2")

main_circ.append(subcirc1,[3,0,2])
main_circ.append(subcirc4,[0,3])
main_circ.append(subcirc1,[1,2,3])
main_circ.append(subcirc4,[1,3])
main_circ.h(1)
main_circ.append(subcirc3,[0,3,1,qreg_0[0],2])
main_circ.append(subcirc1,[2,qreg_0[0],0])
main_circ.cy(0,2)
main_circ.cy(1,2)
main_circ.cy(1,0)
main_circ.cy(2,1)
main_circ.cy(qreg_0[0],1)
main_circ.cy(3,qreg_0[0])
main_circ.cy(1,qreg_0[0])
main_circ.cy(1,qreg_0[0])
main_circ.cy(2,3)
bindings = {}
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
compare_statevectors(main_circ, "Optimize1qGatesDecomposition")
