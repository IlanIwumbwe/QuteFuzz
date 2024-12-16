#ifndef PARAM_H
#define PARAM_H

#include "utils.h"

struct Param{
	std::string name = "", definition_keyword = "";
	bool used = false;
	std::string val;

	Param(){}

	Param(std::string n) {
		name = n;
		val = std::to_string(f_get_rand(-1.0, 1.0));

		set_definition_keyword();
	}

	Param(std::string n, std::string default_val){
		name = n;
		val = default_val;

		set_definition_keyword();
	}

	/// If this param is a symbol, set the correct keyword that should be used to define it based on the front-end
	void set_definition_keyword(){
		if (f == f_qiskit){
			definition_keyword = "Parameter";
		} else if (f == f_pytket){
			definition_keyword = "Symbol";
		}
	}
};

#endif