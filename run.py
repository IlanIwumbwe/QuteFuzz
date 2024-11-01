import subprocess
import argparse
import os 
import sys

QC_DIR = "quantum_circuits"
PLOTS_DIR = os.path.join(QC_DIR, "plots")

def progress_bar(current : int, total : int) -> None:
    # Calculate progress and lengths for the filled and empty parts of the bar
    progress = int((current / total) * 100)
    done = int(progress / 2)  
    left = 50 - done  

    # Build and print the progress bar
    bar = f"\rProgress : [{'▇' * done}{' ' * left}] Circuit {current}/{total}"
    sys.stdout.write(bar)
    sys.stdout.flush()

def setup_dir() -> None:
    if(os.path.exists(QC_DIR)):
        for file in os.listdir(QC_DIR):
            path = os.path.join(QC_DIR, file)
            if(os.path.isfile(path)):
                os.remove(path)
    else:
        os.mkdir(QC_DIR)
        print("Created", QC_DIR, "directory")

def main() -> None:
    parser = argparse.ArgumentParser(description="Runs QuteFuzz generator and differential tester")

    parser.add_argument("frontend", type=str, help="Frontend to generate for ((q)iskit, (c)irq, (p)ytket)", default="p", choices=["qiskit","cirq","pytket","q","c","p"])
    parser.add_argument("num_of_programs", type=str, help="Number of programs to generate")
    parser.add_argument("-v", action="store_true",  help="Verbose adds extra information to the results log file")
    parser.add_argument("-p", action="store_true", help="Plot graphs")

    args = parser.parse_args()

    setup_dir()

    # vars passed to python circuits for verbose results and plotting
    verbose = "-v" if (args.v) else ""
    plot = "-p" if (args.p) else ""

    if(not os.path.exists(PLOTS_DIR) and args.p):
        os.mkdir(PLOTS_DIR)

    # compile the generate
    subprocess.run("make")

    if(os.name == "nt"):
        exe = "gen.exe"
    elif (os.name == "posix"):
        exe = "./gen"

    assert(os.path.exists(exe))

    subprocess.run([exe, "-n", args.num_of_programs, f"-{args.frontend[0]}"])

    current_directory = os.getcwd()
    # export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    if current_directory not in sys.path:
        sys.path.insert(0, current_directory)
        print("Adding project to PYTHONPATH")

    # run circuits
    print("Running cirucits ....")
    for i, file in enumerate(sorted(os.listdir(QC_DIR))):

        if (not os.path.isdir(file) and (file.split(".")[1] == "py")):
            path = os.path.join(QC_DIR, file)
            log_path = os.path.join(QC_DIR, "_results.txt")

            progress_bar(i+1, int(args.num_of_programs))

            with open(log_path, "a") as f:
                
                try:
                    subprocess.run(
                        ["python", "-Wi", path, verbose, plot],
                        stdout=f,
                        stderr=subprocess.STDOUT,
                        check=True
                    )
                except Exception as e:
                    print(f"\nERROR '{e}' occured while running circuits, check", log_path, "for details")

    print("\nResults in ", log_path)

if __name__ == "__main__":

    main()  