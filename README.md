# QuteFuzz
A bug finding tool for quantum compilers.

<p align="center" width="100%">
    <img width="20%" src="images/qutefuzz.png">

QuteFuzz generates circuits for Pytket, Cirq, and Qiskit directly. 

## Contributors

| People | GitHub | Email | 
|--------|--------|-------|
| Benny  | [:octocat:](https://github.com/Bennybenassius) | benny.liu21@imperial.ac.uk |
| Ilan  | [:octocat:](https://github.com/IlanIwumbwe) | ii122@imperial.ac.uk |
| Dr.John Wickerson  | [:octocat:](https://github.com/johnwickerson) | j.wickerson@imperial.ac.uk |

## Bugs found with the help of QuteFuzz

### Pytket:

| Compiler Bugs | Simulator Bugs | Not implemented |
|---------------|----------------|--------|
| [Issue 1553 &#x1F41E;](https://github.com/CQCL/tket/issues/1553)  | [Issue 375 &#x1F41E;](https://github.com/CQCL/pytket-qiskit/issues/375) | 
| [Issue 1566  &#x1F41E;](https://github.com/CQCL/tket/issues/1566) | 
| [Issue 1534  &#x1F41E;](https://github.com/CQCL/tket/issues/1534) (Known) |
| [Issue 1536  &#x1F41E;](https://github.com/CQCL/tket/issues/1536) |
| [Issue 1552  &#x1F41E;](https://github.com/CQCL/tket/issues/1552) | | 
| [Issue 1554  &#x1F41E;](https://github.com/CQCL/tket/issues/1554) | |
| | | [Issue 374 &#x1F41E;](https://github.com/CQCL/pytket-qiskit/issues/374) |

### Qiskit:
| Compiler Bugs | Simulator Bugs |
|---------------|----------------|
| [Issue 13118 &#x1F41E;](https://github.com/Qiskit/qiskit/issues/13118) |  | 
| [Issue 13079 &#x1F41E;](https://github.com/Qiskit/qiskit/issues/13079) |
| [Issue 13162 &#x1F41E;](https://github.com/Qiskit/qiskit/issues/13162) | |
| | [Issue 2230 &#x1F41E;](https://github.com/Qiskit/qiskit-aer/issues/2230) |
| [Issue 13165 &#x1F41E;](https://github.com/Qiskit/qiskit/issues/13165)(Unacknowledged) |  |
|  | [Issue 2215 &#x1F41E;](https://github.com/Qiskit/qiskit-aer/issues/2215)(Unacknowledged) |

### Cirq:

| Compiler Bugs | Simulator Bugs | Circuit Construction |
|---------------|----------------|--------|
|               | [Issue 6730 &#x1F41E;](https://github.com/quantumlib/Cirq/issues/6730) | 
| | | [Issue 6727 &#x1F41E;](https://github.com/quantumlib/Cirq/issues/6727) | 
| [Issue 6507 &#x1F41E;](https://github.com/quantumlib/Cirq/issues/6507) (Known) | | |



## Running the fuzzer

### Set up a docker environment

If you already have a Linux environment, skip to step 6

1. You need to install docker on your system. Follow these [installation steps](https://docs.docker.com/get-started/get-docker/) to do so.
2. Clone this repository
3. Navigate into the repository, and setup a docker image using:
    ``` sh
    docker build -t qutefuzz .
    ```
4. Create and start a docker container based on the image using: 
    ```sh 
    docker run -v ./quantum_circuits:/qutefuzz/quantum_circuits -it --rm qutefuzz
    ``` 
    This should open up a terminal through which you will be able to interact with the container.
5. Activate the python virtual environment using:
    ```sh
    source .qutefuzz/bin/activate
    ```
6. Install python dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Generate and run circuits

- Use `./run.sh` to generate and run circuits. To see all available flags, use `./run.sh -h`.
- You can run the generator on its own by compiling using `make`. Generate n circuits using:
    ```sh
    ./gen -n {n}
    ```
- Full usage: `./gen -n {programs to generate} [-q/-p/-c] [-d]`

All quantum circuits, logs and results will be shown in a `quantum_circuits` folder in the repo directory

