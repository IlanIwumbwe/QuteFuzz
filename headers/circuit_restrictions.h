#ifndef CIRCUIT_RESTRICTIONS_H
#define CIRCUIT_RESTRICTIONS_H

#include "utils.h"
#include "gate.h"

struct Circuit_Restrictions{
	std::string name;
	ULL gateset_flag;
	unsigned int restriction = 0;
    std::vector<Gate> gateset;

	Circuit_Restrictions(){}
	Circuit_Restrictions(std::string n, ULL gsf) : name(n), gateset_flag(gsf){}
	Circuit_Restrictions(std::string n, ULL gsf, unsigned int r) : name(n), gateset_flag(gsf), restriction(r){}
};

#endif
