from setuptools import setup

setup(
    name='qutefuzz_helpers',
    description='Differential testing for qiskit, cirq and pytket circuits. Used by QuteFuzz',
    url='https://github.com/IlanIwumbwe/QuteFuzz',
    license='MIT',
    version='0.1',
    author='Benny and Ilan',
    packages=['helpers'],
    install_requires=['qiskit', 'pytket', 'cirq', 'pytket-qiskit', 'matplotlib', 'sympy', 'z3-solver'],
)
