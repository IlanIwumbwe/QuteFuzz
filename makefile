CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O3
SRCS = $(wildcard src/*.cpp) 
OBJS = $(SRCS:.cpp=.o)
TARGET = gen
	
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

all: $(TARGET)

.PHONY: clean

clean:
	rm -f $(OBJS) $(TARGET)
	rm -rf quantum_circuits
