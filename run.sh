#! /bin/bash

dir=quantum_circuits
plot_dir=plots

if [ ! -d $dir ] 
then
    mkdir $dir
else
    rm -rf $dir/*
fi

function ProgressBar {
    # Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*5)/10
    let _left=50-$_done
    # Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

    # Build progressbar strings and print the ProgressBar line
    printf "\rProgress : [${_fill// /▇}${_empty// / }] Circuit ${1}/${2}"
}

print_usage() {
    echo -e "Usage: ./build.sh [-p] [-v]"
    echo -e "The -v flag makes the quantum_circuits/_results.txt file more verbose, as well as put circuit generation information into quantum_circuits/log.txt"
    echo -e "The -p will plot the probability distributions after running the circuits."
}

print_questions(){
    echo "How many programs should be generated: "
    read x

    echo "Front-end to generate for (qiskit(q)/pytket(p)/cirq(c)): "
    read f
}

while getopts 'pvh' flag; do
    case ${flag} in
        v) v="-v" ;;
        p) p="-p"
           mkdir "$dir/$plot_dir"
        ;;
        h) print_usage 
            exit 1;;
        *) print_usage
            exit 1;;
    esac
done

make
print_questions

if [[ v = "-v" ]] 
then
    ./gen -n "$x" "-$f" -d >> "quantum_circuits/log.txt"
else
    ./gen -n "$x" "-$f"
fi

if [[ ":$PYTHONPATH:" != *":$(pwd):"* ]]; then
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    echo "Adding project to PYTHONPATH" 
fi

for ((i = 1; i <= $x; i++))
do
    ProgressBar ${i} ${x}
    python3 -Wi "quantum_circuits/circuit$i.py" "$v" "$p" >> "quantum_circuits/_results.txt"
done

echo -e "\nDone"