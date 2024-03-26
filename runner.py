import subprocess
import time
import os

RUST_DIRECTORY = "rust"
GO_DIRECTORY = "go"
ZIG_DIRECTORY = "zig"

def get_portable_binary_name(binary_name: str) -> str:
    """
    Returns the portable binary name for the given binary name

    Args:
        binary_name (str): The binary name

    Returns:
        str: The portable binary name

    """
    return binary_name + ".exe" if os.name == "nt" else binary_name

def build_rust_program():
    """
    Builds the Rust program and returns the path to the executable

    Returns:
        str: Path to the Rust executable

    """
    
    os.system(f"cd {RUST_DIRECTORY} && cargo build --release")

    return os.path.join(RUST_DIRECTORY, "target", "release", get_portable_binary_name("rust-benchmark"))

def build_go_program():
    """
    Builds the Go program and returns the path to the executable

    Returns:
        str: Path to the Go executable

    """
    os.system(f"cd {GO_DIRECTORY} && make build")

    return os.path.join(GO_DIRECTORY, get_portable_binary_name("go-benchmark"))

def build_zig_program():
    """
    Builds the Zig program and returns the path to the executable

    Returns:
        str: Path to the Zig executable

    """
    os.system(f"cd {ZIG_DIRECTORY} && zig build")

    return os.path.join(ZIG_DIRECTORY, "zig-out", "bin", get_portable_binary_name("zig-benchmark"))

def benchmark(program_path, num_runs=10):
    execution_times = []
    for _ in range(num_runs):
        start_time = time.time()
        subprocess.run(program_path, shell=True)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times

def main():
    # Build the Rust program
    rust_program_path = build_rust_program()
    go_program_path = build_go_program()
    zig_program_path = build_zig_program()

    if not rust_program_path:
        raise Exception("Failed to build Rust program")
    if not go_program_path:
        raise Exception("Failed to build Go program")
    if not zig_program_path:
        raise Exception("Failed to build Zig program")
    

    print("Rust Program Path:", rust_program_path)
    print("Go Program Path:", go_program_path)
    print("Zig Program Path:", zig_program_path)


    # Benchmark each program
    go_execution_times = benchmark(go_program_path)
    rust_execution_times = benchmark(rust_program_path)
    zig_execution_times = benchmark(zig_program_path)

    # Display results
    print("Go Program Execution Times:", go_execution_times)
    print("Rust Program Execution Times:", rust_execution_times)
    print("Zig Program Execution Times:", zig_execution_times)

    return



if __name__ == "__main__":
    main()
