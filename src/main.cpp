#include <unistd.h>
#include "../headers/generator.h"

void usage(){
	std::cout << "Usage ./gen -n {programs to generate} [-q/-p/-c]" << std::endl;
}

int get_files_to_generate(char* argv[]){
	int n = 0;

	try{
		n = std::stoi(argv[2]);
	} catch (...) {
		std::cout << "Number of files to generate passed should be an integer, 1 program will be generated" << std::endl;
		n = 1;
	}

	return n;
}

int main(int argc, char* argv[]) {
	int files_to_generate = 0;
	
	switch(argc){
		case 5:
			if(((std::string)argv[1] == "-n")){
				files_to_generate = get_files_to_generate(argv);
				
				if((std::string)argv[3] == "-q"){
					f = f_qiskit;
				} else if ((std::string)argv[3] == "-c"){
					f = f_cirq;
				}

				generate(files_to_generate);
			}

			break;
		
		case 4:
			if(((std::string)argv[1] == "-n")){
				files_to_generate = get_files_to_generate(argv);
		
				if((std::string)argv[3] == "-q"){
					f = f_qiskit;
				} else if ((std::string)argv[3] == "-c"){
					f = f_cirq;
				}

				generate(files_to_generate);
			}

			break;

		case 3:
			if(((std::string)argv[1] == "-n")){
				files_to_generate = get_files_to_generate(argv);
			}

			generate(files_to_generate);

			break;

		default:
			usage();
			return -1;
	
	}
	
	return 0;
}