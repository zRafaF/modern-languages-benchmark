# Compiler settings - Can change to gcc, clang, etc.
CXX := g++
# Compiler flags, e.g., CXXFLAGS += -std=c++11 for C++11 support
CXXFLAGS += -Iinclude -Wall -g -fopenmp

PROGRAM := c-benchmark

# If the first command in a recipe fails, just return an error
# rather than continuing with other commands
.ONESHELL:

# Define .cpp source files
SOURCES := $(wildcard src/*.c)

# Define the output program
TARGET := bin/$(PROGRAM)

# Platform-specific modifications
ifeq ($(OS),Windows_NT)
    RM = del /Q
    FixPath = $(subst /,\,$1)
    TARGET := $(TARGET).exe
else
    RM = rm -f
    FixPath = $1
endif

# Default make
all: $(TARGET)

# Link the target with all object files (force recompile every time)
$(TARGET): $(SOURCES)
	@mkdir -p bin
	$(CXX) $(CXXFLAGS) -o $@ $(SOURCES)

# Clean up build files
clean:
	$(RM) $(call FixPath,bin/*)

run: all
	./$(TARGET)



.PHONY: all clean run


