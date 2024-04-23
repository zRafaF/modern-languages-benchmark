from argparse import ArgumentParser
from enum import Enum


class LanguagesEnum(Enum):
    GO = 1
    RUST = 2
    ZIG = 3


class BenchmarkTypeEnum(Enum):
    BUBBLE_SORT = 1
    GAUSSIAN_BLUR_SEQ = 2
    GAUSSIAN_BLUR_PAR = 3


parser = ArgumentParser()
parser.add_argument(
    "-g",
    "--generate",
    help="Generates the vector file (File used as input for the benchmarks)",
    default=False,
    action="store_true",
)

parser.add_argument(
    "-r",
    "--run",
    help="Runs the benchmark",
    default=False,
    action="store_true",
)

parser.add_argument(
    "-t",
    "--type",
    help="Type of benchmark to run\n 1: Bubble Sort\n 2: Gaussian Blur Sequential\n 3: Gaussian Blur Parallel",
    default=1,
    type=int,
)

parser.add_argument(
    "-b",
    "--build",
    help="Builds the programs",
    default=False,
    action="store_true",
)

parser.add_argument(
    "--go",
    help="Runs the benchmark for the Go program",
    default=False,
    action="store_true",
)

parser.add_argument(
    "--rust",
    help="Runs the benchmark for the Rust program",
    default=False,
    action="store_true",
)

parser.add_argument(
    "--zig",
    help="Runs the benchmark for the Zig program",
    default=False,
    action="store_true",
)

parser.add_argument(
    "--iterations",
    help="Number of iterations for the benchmark",
    default=1,
    type=int,
)

args = parser.parse_args()


class Arguments:
    def __init__(self):

        self.generate: bool = args.generate
        self.run: bool = args.run
        self.build: bool = args.build
        self.iterations: int = args.iterations
        self.target_languages = self._get_target_languages()
        self.benchmark_type = self._get_benchmark_type()

    def _get_benchmark_type(self) -> BenchmarkTypeEnum:
        if args.type == 1:
            return BenchmarkTypeEnum.BUBBLE_SORT
        elif args.type == 2:
            return BenchmarkTypeEnum.GAUSSIAN_BLUR_SEQ
        elif args.type == 3:
            return BenchmarkTypeEnum.GAUSSIAN_BLUR_PAR
        else:
            raise Exception("Invalid benchmark type")

    def _get_target_languages(self) -> list[LanguagesEnum]:
        langs = []
        if args.go:
            langs.append(LanguagesEnum.GO)
        if args.rust:
            langs.append(LanguagesEnum.RUST)
        if args.zig:
            langs.append(LanguagesEnum.ZIG)

        return langs


arguments = Arguments()
