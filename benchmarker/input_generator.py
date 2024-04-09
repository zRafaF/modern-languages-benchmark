import random
import os.path
import numpy as np
from PIL import Image

INPUT_FILES_PATH = "input_files"

VECTOR_INPUT_PATH = os.path.join(os.getcwd(), INPUT_FILES_PATH, "vector_input.txt")
IMAGE_INPUT_PATH = os.path.join(os.getcwd(), INPUT_FILES_PATH, "image_input.raw")


def does_input_files_exist():
    """
    Checks if the input files exist

    """

    if not os.path.exists(VECTOR_INPUT_PATH) or not os.path.exists(IMAGE_INPUT_PATH):
        return False
    return True


def generate_image_file():
    """
    Generates the image file (File used as input for the benchmarks)

    returns:
        str: Path to the generated image file
    """

    # Generate random noise data
    noise = np.random.randint(0, 256, (512, 512), dtype=np.uint8)

    noise.tofile(IMAGE_INPUT_PATH)
    # # Create PIL image from the noise data
    # img = Image.fromarray(noise, mode="L")  # 'L' mode for grayscale

    # # Save the image to a file
    # img.save(IMAGE_INPUT_PATH)

    return IMAGE_INPUT_PATH


def generate_sorting_vector_file():
    """
    Generates the vector file (File used as input for the benchmarks)

    returns:
        str: Path to the generated vector file
    """

    min_rand_number = 0
    max_rand_number = 1000

    quantity = 100000

    # creates a file named inputfiles/vector_input.txt and fills it with a vector with random numbers
    with open(VECTOR_INPUT_PATH, "w") as f:
        f.write(
            " ".join(
                [
                    str(random.uniform(min_rand_number, max_rand_number))
                    for _ in range(quantity)
                ]
            )
        )
    return VECTOR_INPUT_PATH


def generate_input_files():
    """
    Generates the input files

    """
    if not os.path.exists(INPUT_FILES_PATH):
        print("Input files directory does not exist, creating it...")
        os.mkdir(INPUT_FILES_PATH)

    generate_image_file()
    generate_sorting_vector_file()
