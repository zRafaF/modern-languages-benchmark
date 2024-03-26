import subprocess
import time
import os

RUST_DIRECTORY = "rust"
GO_DIRECTORY = "go"
ZIG_DIRECTORY = "zig"


def build_rust_program():
    """
    Builds the Rust program and returns the path to the executable

    Returns:
        str: Path to the Rust executable

    """
    
    os.system(f"cd {RUST_DIRECTORY} && cargo build --release")
    # Program name is rust-benchmark on linux and rust-benchmark.exe on windows
    program_name: str = "rust-benchmark" if os.name == "posix" else "rust-benchmark.exe"

    return os.path.join(RUST_DIRECTORY, "target", "release", program_name)

def benchmark(program_path, num_runs=10):
    execution_times = []
    for _ in range(num_runs):
        start_time = time.time()
        subprocess.run(program_path, shell=True)  # Replace with appropriate command for execution
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times

def main():
    # Build the Rust program
    rust_program_path = build_rust_program()
    if not rust_program_path:
        raise Exception("Failed to build Rust program")
    
    rust_execution_times = benchmark(rust_program_path)

    print("Rust Program Execution Times:", rust_execution_times)


    return
    # Paths to the programs you want to benchmark
    go_program_path = "path/to/your/go/program"
    rust_program_path = "path/to/your/rust/program"
    python_program_path = "path/to/your/python/program"

    # Benchmark each program
    go_execution_times = benchmark(go_program_path)
    rust_execution_times = benchmark(rust_program_path)
    python_execution_times = benchmark(python_program_path)

    # Display results
    print("Go Program Execution Times:", go_execution_times)
    print("Rust Program Execution Times:", rust_execution_times)
    print("Python Program Execution Times:", python_execution_times)

if __name__ == "__main__":
    main()
