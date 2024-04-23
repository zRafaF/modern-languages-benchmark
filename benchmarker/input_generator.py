import random
import os.path
import numpy as np

INPUT_FILES_PATH = "input_files"

IMAGE_INPUT_PATH = os.path.join(os.getcwd(), INPUT_FILES_PATH, "image_input.raw")


def does_input_files_exist():
    """
    Checks if the input files exist

    """

    if not os.path.exists(IMAGE_INPUT_PATH):
        return False
    return True


def generate_image_file():
    """
    Generates the image file (File used as input for the benchmarks)

    returns:
        str: Path to the generated image file
    """

    # Generate a 256x256 with random noise
    noise = np.random.randint(0, 256, (256 * 256), dtype=np.uint8)

    with open(IMAGE_INPUT_PATH, "wb") as f:
        f.write(noise.tobytes())

    print(f"First byte: {noise[0]} Last byte: {noise[-1]}")

    return IMAGE_INPUT_PATH


def generate_input_files():
    """
    Generates the input files

    """
    if not os.path.exists(INPUT_FILES_PATH):
        print("Input files directory does not exist, creating it...")
        os.mkdir(INPUT_FILES_PATH)

    generate_image_file()
