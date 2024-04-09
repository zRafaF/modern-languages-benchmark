# Define the default Python interpreter
PYTHON := python

# Detect if the OS is Linux
ifeq ($(shell uname),Linux)
    PYTHON := python3
endif

ITERATIONS ?= 10

.PHONY: run build generate install

# Target to run the Python program after building
run: 
	@echo "Running the Python benchmark..."
	$(PYTHON) benchmarker/main.py -r --go --zig --rust --iterations=$(ITERATIONS)

run-go:
	@echo "Running the Go benchmark..."
	$(PYTHON) benchmarker/main.py -r --go --iterations=$(ITERATIONS)

run-zig:
	@echo "Running the Zig benchmark..."
	$(PYTHON) benchmarker/main.py -r --zig --iterations=$(ITERATIONS)

run-rust:
	@echo "Running the Rust benchmark..."
	$(PYTHON) benchmarker/main.py -r --rust --iterations=$(ITERATIONS)



# Target to run the Python program after building
run-fresh: generate build run
	@echo "Running a fresh benchmark..."


# Target to build the Python program
build:
	@echo "Building the programs..."
	$(PYTHON) benchmarker/main.py -b

# Target to generate input files
generate:
	@echo "Generating input files..."
	$(PYTHON) benchmarker/main.py -g

install:
	$(PYTHON) -m pip install -r benchmarker/requirements.txt
