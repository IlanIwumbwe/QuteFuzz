#ifndef UTILS_H
#define UTILS_H

#include <fstream>
#include <iostream>
#include <random>
#include <assert.h>
#include <filesystem>
#include <bitset>
#include <math.h>
#include <unordered_map>
#include <vector>
#include "defs.h"

#define get_lsb(number) __builtin_ctzll(number)

// constants 
const int SUPPORTED_FRONTENDS = 3;

/// minimum should be at least 4 because generator supports some gates that use 4 qubits, and they could be the only gates in the circuit's gateset
const int MIN_TOTAL_QUBITS = 4; 
const int MAX_TOTAL_QUBITS = 50;
const int MIN_TOTAL_GATES = 70;
const int MAX_TOTAL_GATES = 150;

const int MIN_CIRCBOX_GATES = 4;
const int MAX_CIRCBOX_GATES = 6;
const int MAX_CIRCBOX_CONTROL_QUBITS = 3;
const int MAX_CIRCB0XES = 15;

const int N_INIT_BITS = 2;
const int N_NAMED_BITS = 2;
const float C_GATE_RATIO = 0.3;

extern fs::path CIRCUITS_DIR;
extern frontend f;

/// return a random number given a lower and upper bound (int)
inline int get_rand(int lb, int ub){

    if(lb <= ub){
        std::random_device rd;
        std::mt19937 gen(rd());

        std::uniform_int_distribution<> dis(lb, ub);

        int random_number = dis(gen);
        
        return random_number;
    }
    else{
        std::cerr << "Lb is greater than ub" << std::endl;
        return 0;
    }
}

/// return a random number between lower and upper bound (float)
inline float f_get_rand(float lb, float ub){
    float denominator = 1000.0;
    int i_lb = lb * denominator;
    int i_ub = ub * denominator;

    return (float)get_rand(i_lb, i_ub) / denominator;
}

std::bitset<4> numtobin(U4& number);

template<typename T>
void v_append(std::vector<T>& v1, std::vector<T>& v2);

template<typename T>
bool v_exists(std::vector<T> vec, T val);

std::string get_gate_name(gate_type t);

#endif