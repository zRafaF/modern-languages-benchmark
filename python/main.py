import sys
import numpy as np
from boxblur import sequential, parallel
from PIL import Image


class BenchmarkType:
    BUBBLE_SORT = 1
    BOX_BLUR_SEQUENTIAL = 2
    BOX_BLUR_PARALLEL = 3


def save_to_file(data, filename):
    data.tofile(filename)


def load_image(image_path):
    # loads a .raw file file as a numpy array
    with open(image_path, "rb") as file:
        image = np.fromfile(file, dtype=np.uint8)
    return np.array(image, dtype=np.uint8)


def main():
    if len(sys.argv) < 3:
        print(
            "Error: Not enough arguments\nUsage: python main.py <image-path> <benchmark-type>\nbenchmark-type: (2=Box Blur Sequential) (3=Box Blur Parallel)"
        )
        sys.exit(1)

    image_path = sys.argv[1]
    benchmark_type = int(sys.argv[2])

    if not image_path:
        print("Error: No image path specified")
        sys.exit(1)

    try:
        data = load_image(image_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    if benchmark_type == BenchmarkType.BOX_BLUR_SEQUENTIAL:
        result = sequential(data)
    elif benchmark_type == BenchmarkType.BOX_BLUR_PARALLEL:
        result = parallel(data)
    else:
        print("Error: Invalid benchmark type")
        sys.exit(1)

    save_to_file(result, "python_result.raw")


if __name__ == "__main__":
    main()
