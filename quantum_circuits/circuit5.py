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
subcirc0.u(0,0,0.975000, qreg_0[0])
subcirc0.rx(-0.637000, qreg_1[0])
subcirc0.u(pi/2,-0.226000,0.797000, qreg_0[0])
subcirc0.u(-0.286000,0.957000,0.927000, qreg_1[0])
subcirc0.u(-0.899000,0.866000,0.311000, qreg_0[0])
subcirc0.u(pi/2,-0.911000,0.385000, qreg_1[0])
subcirc0 = subcirc0.to_gate().control(1)

main_circ = QuantumCircuit(0)
# Adding qregs 
qreg_0 = QuantumRegister(2)
main_circ.add_register(qreg_0)
qreg_2 = QuantumRegister(2)
main_circ.add_register(qreg_2)
# Adding creg resources 
creg_0 = ClassicalRegister(2)
main_circ.add_register(creg_0)
# Adding symbols 
param_0 = Parameter("param_0")
param_1 = Parameter("param_1")
param_2 = Parameter("param_2")
param_3 = Parameter("param_3")

main_circ.append(subcirc0,[qreg_2[0],qreg_2[1],qreg_0[0]])
main_circ.u(param_3,-0.157000,param_3, qreg_0[1])
main_circ.u(pi/2,param_3,param_3, qreg_2[0])
main_circ.append(subcirc0,[qreg_2[0],qreg_2[1],qreg_0[1]])
main_circ.u(0,0,-0.663000, qreg_0[0])
main_circ.u(pi/2,param_2,0.173000, qreg_2[0])
main_circ.append(subcirc0,[qreg_2[0],qreg_2[1],qreg_0[0]])
main_circ.u(pi/2,param_3,param_2, qreg_2[1])
main_circ.rx(param_2, qreg_2[1])
main_circ.append(subcirc0,[qreg_2[0],qreg_2[1],qreg_0[1]])
main_circ.u(param_1,param_3,param_2, qreg_2[0])
main_circ.u(param_0,-0.332000,-0.542000, qreg_2[0])
main_circ.u(-0.248000,-0.562000,0.021000, qreg_2[1])
main_circ.u(0,param_0,param_1, qreg_2[0])
main_circ.u(0,0,0.463000, qreg_0[0])
main_circ.append(subcirc0,[qreg_0[0],qreg_2[1],qreg_0[1]])
main_circ.rx(-0.261000, qreg_0[1])
main_circ.rx(param_3, qreg_0[0])
main_circ.u(param_1,-0.273000,param_3, qreg_2[0])
bindings = {param_0: 0.769000, param_1: -0.072000, param_2: 0.233000, param_3: 0.768000, }
main_circ = main_circ.assign_parameters(bindings)

print(Path(__file__).name, " results:")
compare_statevectors(main_circ, "Collect1qRuns")
