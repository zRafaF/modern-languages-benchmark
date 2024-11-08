import os
import subprocess
import time
from builder import Builder
from input_generator import (
    generate_input_files,
    does_input_files_exist,
    generate_noise,
    IMAGE_INPUT_PATH,
)
import sys
from arguments import arguments, LanguagesEnum
from viewer import plot_image_from_raw_file

RUST_DIRECTORY = os.path.join(os.getcwd(), "rust")
GO_DIRECTORY = os.path.join(os.getcwd(), "go")
ZIG_DIRECTORY = os.path.join(os.getcwd(), "zig")
PYTHON_DIRECTORY = os.path.join(os.getcwd(), "python")
C_DIRECTORY = os.path.join(os.getcwd(), "c")


def benchmark(
    program_path: str, args: list[str], iterations: int, is_python: bool = False
):
    execution_times = []
    for it in range(iterations):
        print(f"Iteration: {it}")
        start_time = time.time()
        if is_python:
            current_env = os.environ.copy()
            subprocess.run([sys.executable, program_path, *args], env=current_env)
        else:
            subprocess.run([program_path, *args])
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times


def run_benchmark(target_language: LanguagesEnum, iterations: int):
    builder = Builder(
        RUST_DIRECTORY, ZIG_DIRECTORY, GO_DIRECTORY, PYTHON_DIRECTORY, C_DIRECTORY
    )

    build_path: str = ""

    match target_language:
        case LanguagesEnum.GO:
            build_path = builder.go_build_path
        case LanguagesEnum.RUST:
            build_path = builder.rust_build_path
        case LanguagesEnum.ZIG:
            build_path = builder.zig_build_path
        case LanguagesEnum.PYTHON:
            build_path = builder.python_build_path
        case LanguagesEnum.C:
            build_path = builder.c_build_path

        case _:
            raise Exception("No target language provided")

    if not does_input_files_exist():
        raise Exception("Input files do not exist. Please generate them first.")

    if not builder.does_build_exist(target_language):
        raise Exception("Build does not exist. Please build it first.")

    args = [
        f"{IMAGE_INPUT_PATH}",
        f"{arguments.benchmark_type.value}",
    ]

    print(build_path)

    return benchmark(
        build_path, args, iterations, target_language == LanguagesEnum.PYTHON
    )


def main():
    if arguments.output_file:
        plot_image_from_raw_file(arguments.output_file)
        return

    if arguments.build:
        builder = Builder(
            RUST_DIRECTORY, ZIG_DIRECTORY, GO_DIRECTORY, PYTHON_DIRECTORY, C_DIRECTORY
        )
        for targ_lang in arguments.target_languages:
            match targ_lang:
                case LanguagesEnum.GO:
                    builder.build_go_program()
                case LanguagesEnum.RUST:
                    builder.build_rust_program()
                case LanguagesEnum.ZIG:
                    builder.build_zig_program()
                case LanguagesEnum.C:
                    builder.build_c_program()
        return

    if arguments.generate:
        generate_input_files()
        print("Input files generated.")
        return

    if arguments.run:
        results = []
        for targ_lang in arguments.target_languages:
            print(f"Running benchmark for {targ_lang}")
            exec_times = run_benchmark(targ_lang, arguments.iterations)
            results.append((targ_lang, exec_times))
        print(results)

        total_times = sum(exec_times)

        print(f"Average time: {total_times/arguments.iterations}")

        return

    raise Exception(
        "No main (run, generate, build) arguments provided. Use -h or --help for help."
    )


if __name__ == "__main__":
    main()
