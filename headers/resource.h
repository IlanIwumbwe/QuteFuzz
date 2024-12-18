#ifndef RESOURCE_H
#define RESOURCE_H

#include <string>
#include <vector>

struct Resource{
	resource_type rt;
	std::string str;

	std::pair<std::string, int> _reg;
	bool used = false;
	int times_used = 0;
	bool bad_choice_for_replacement = false;

	std::vector<Resource> concurrent_resources;

	Resource (){}

	Resource(resource_type t, std::string s) :rt(t), str(s) {}
	
	bool operator==(Resource rp){
		return (rt == rp.rt) && (str == rp.str);
	}

	friend std::ostream& operator<<(std::ostream& os, Resource& r){
		os << r.str << ", times used: " << r.times_used << ", used:" << r.used <<  std::endl;

		if(r.concurrent_resources.size()){
			os << "=> concurrent resources:" << std::endl;
			for(Resource& other_r : r.concurrent_resources){
				os << "\t" << other_r.str << std::endl;
			}
		}

		return os;
	}

	/// @brief Transfer concurreny information from the resource `r` to this resource	
	/// @param r 
	void get_concurrencies(Resource& r){
		concurrent_resources.insert(concurrent_resources.end(), r.concurrent_resources.begin(), r.concurrent_resources.end());
	}

};

#endif