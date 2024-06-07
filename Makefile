# Define the default Python interpreter
PYTHON := python

# Detect if the OS is Linux
ifeq ($(shell uname),Linux)
    PYTHON := python3
endif

ITERATIONS ?= 10
TYPE ?= 1

.PHONY: run build generate install

# Target to run the Python program after building
run: 
	@echo "Running the Python benchmark..."
	$(PYTHON) benchmarker/main.py -r --go --zig --rust --iterations=$(ITERATIONS) -t=$(TYPE)

run-go:
	@echo "Running the Go benchmark..."
	$(PYTHON) benchmarker/main.py -r --go --iterations=$(ITERATIONS) -t=$(TYPE)

run-zig:
	@echo "Running the Zig benchmark..."
	$(PYTHON) benchmarker/main.py -r --zig --iterations=$(ITERATIONS) -t=$(TYPE)

run-rust:
	@echo "Running the Rust benchmark..."
	$(PYTHON) benchmarker/main.py -r --rust --iterations=$(ITERATIONS) -t=$(TYPE)

run-python:
	echo "Running the Python benchmark..."
	$(PYTHON) benchmarker/main.py -r --python --iterations=$(ITERATIONS) -t=$(TYPE)

# Target to run the Python program after building
run-fresh: build run
	@echo "Running a fresh benchmark..."


run-go-fresh: build-go run-go
	@echo "Running a fresh Go benchmark..."

run-zig-fresh: build-zig run-zig
	@echo "Running a fresh Zig benchmark..."

run-rust-fresh: build-rust run-rust
	@echo "Running a fresh Rust benchmark..."

run-python-fresh: run-python
	echo "Running a fresh Python benchmark..."


# Target to build the Python program
build:
	@echo "Building the programs..."
	$(PYTHON) benchmarker/main.py -b --go --zig --rust

build-go:
	@echo "Building the Go program..."
	$(PYTHON) benchmarker/main.py -b --go

build-zig:
	@echo "Building the Zig program..."
	$(PYTHON) benchmarker/main.py -b --zig

build-rust:
	@echo "Building the Rust program..."
	$(PYTHON) benchmarker/main.py -b --rust

# Target to generate input files
generate:
	@echo "Generating input files..."
	$(PYTHON) benchmarker/main.py -g

install:
	$(PYTHON) -m pip install -r benchmarker/requirements.txt


show-input:
	$(PYTHON) benchmarker/main.py --output=input_files/image_input.raw

show-zig:
	$(PYTHON) benchmarker/main.py --output=zig_result.raw

show-go:
	$(PYTHON) benchmarker/main.py --output=go_result.raw

show-rust:
	$(PYTHON) benchmarker/main.py --output=rust_result.raw

show-python:
	$(PYTHON) benchmarker/main.py --output=python_result.raw