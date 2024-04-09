import subprocess
import time
import os

from argparse import ArgumentParser

from builder import Builder
from generator import generate_sorting_vector_file

parser = ArgumentParser()
parser.add_argument(
    "-g",
    "--generate",
    help="Generates the vector file (File used as input for the benchmarks)",
    default=False,
    action="store_true",
)

args = parser.parse_args()


RUST_DIRECTORY = "rust"
GO_DIRECTORY = "go"
ZIG_DIRECTORY = "zig"


def benchmark(program_path, num_runs=10):
    execution_times = []
    for _ in range(num_runs):
        start_time = time.time()
        subprocess.run(program_path, shell=True)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times


def check_for_input_files():
    if not os.path.exists("inputfiles"):
        os.mkdir("inputfiles")
    if not os.path.exists("inputfiles/vector_input.txt"):
        generate_sorting_vector_file()

def run_benchmark():
    check_for_input_files()

    builder = Builder(RUST_DIRECTORY, ZIG_DIRECTORY, GO_DIRECTORY)

    # Build the Rust program
    rust_program_path = builder.build_rust_program()
    go_program_path = builder.build_go_program()
    zig_program_path = builder.build_zig_program()

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


def main():
    if args.generate:
        generate_sorting_vector_file()
        return

    run_benchmark()
    return


if __name__ == "__main__":
    main()
