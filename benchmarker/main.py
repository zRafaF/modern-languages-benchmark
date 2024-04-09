import os
import subprocess
import time
from builder import Builder
from input_generator import (
    generate_input_files,
    does_input_files_exist,
    IMAGE_INPUT_PATH,
)

from arguments import arguments, LanguagesEnum

RUST_DIRECTORY = os.path.join(os.getcwd(), "rust")
GO_DIRECTORY = os.path.join(os.getcwd(), "go")
ZIG_DIRECTORY = os.path.join(os.getcwd(), "zig")


def benchmark(program_path: str, args: list[str], iterations: int):
    execution_times = []
    for _ in range(iterations):
        start_time = time.time()
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
    ]

    match target_language:
        case LanguagesEnum.GO:
            return benchmark(go_program_path, args, iterations)
        case LanguagesEnum.RUST:
            return benchmark(rust_program_path, args, iterations)
        case LanguagesEnum.ZIG:
            return benchmark(zig_program_path, args, iterations)

        case None:
            raise Exception("No target language provided")


def main():
    if arguments.build:
        builder = Builder(RUST_DIRECTORY, ZIG_DIRECTORY, GO_DIRECTORY)
        for targ_lang in arguments.target_languages:
            match targ_lang:
                case LanguagesEnum.GO:
                    builder.build_go_program()
                case LanguagesEnum.RUST:
                    builder.build_rust_program()
                case LanguagesEnum.ZIG:
                    builder.build_zig_program()
        return

    if arguments.generate:
        generate_input_files()
        return

    if arguments.run:
        results = []
        for targ_lang in arguments.target_languages:
            print(f"Running benchmark for {targ_lang}")
            results.append((targ_lang, run_benchmark(targ_lang, arguments.iterations)))
        print(results)
        return

    raise Exception(
        "No main (run, generate, build) arguments provided. Use -h or --help for help."
    )


if __name__ == "__main__":
    main()
