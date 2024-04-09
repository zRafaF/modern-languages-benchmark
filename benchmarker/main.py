import os
import subprocess
import time
from builder import Builder
from input_generator import (
    generate_input_files,
    does_input_files_exist,
    IMAGE_INPUT_PATH,
    VECTOR_INPUT_PATH,
)

from arguments import arguments, LanguagesEnum

RUST_DIRECTORY = os.path.join(os.getcwd(), "rust")
GO_DIRECTORY = os.path.join(os.getcwd(), "go")
ZIG_DIRECTORY = os.path.join(os.getcwd(), "zig")


def benchmark(program_path: str, args: list[str], iterations: int):
    execution_times = []
    for _ in range(iterations):
        start_time = time.time()
        # Run the program
        subprocess.run([program_path, *args])
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times


def run_benchmark(target_language: LanguagesEnum, iterations: int):
    builder = Builder(RUST_DIRECTORY, ZIG_DIRECTORY, GO_DIRECTORY)

    # Build the Rust program
    rust_program_path = builder.rust_build_path
    go_program_path = builder.go_build_path
    zig_program_path = builder.zig_build_path

    print("Rust Program Path:", rust_program_path)
    print("Go Program Path:", go_program_path)
    print("Zig Program Path:", zig_program_path)

    if not does_input_files_exist():
        raise Exception("Input files do not exist. Please generate them first.")

    if not builder.does_builds_exist():
        raise Exception("Builds do not exist. Please build them first.")

    args = [
        IMAGE_INPUT_PATH,
        VECTOR_INPUT_PATH,
    ]

    match target_language:
        case LanguagesEnum.GO:
            go_execution_times = benchmark(go_program_path, args, iterations)
            print("Go Program Execution Times:", go_execution_times)

        case LanguagesEnum.RUST:
            rust_execution_times = benchmark(rust_program_path, args, iterations)
            print("Rust Program Execution Times:", rust_execution_times)

        case LanguagesEnum.ZIG:
            zig_execution_times = benchmark(zig_program_path, args, iterations)
            print("Zig Program Execution Times:", zig_execution_times)

        case None:
            raise Exception("No target language provided")


def main():
    if arguments.build:
        builder = Builder(RUST_DIRECTORY, ZIG_DIRECTORY, GO_DIRECTORY)
        builder.build_all_programs()
        return

    if arguments.generate:
        generate_input_files()
        return

    if arguments.run:
        for targ_lang in arguments.target_languages:
            print(f"Running benchmark for {targ_lang}")
            run_benchmark(targ_lang, arguments.iterations)
        return

    raise Exception("No arguments provided. Use -h or --help for help.")


if __name__ == "__main__":
    main()
