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


def generate_noise(size: int):
    """
    Generates the image file (File used as input for the benchmarks)

    returns:
        str: Path to the generated image file
    """
    np.random.seed(1234)

    # Generate a 256x256 with random noise
    noise = np.random.randint(0, 256, (size, size), dtype=np.uint8)

    return noise


def generate_check_board():
    size = 512
    block_size = size // 8

    checkboard = np.zeros((size, size), dtype=np.uint8)

    # Fill the checkerboard
    for i in range(0, size, block_size):
        for j in range(0, size, block_size):
            # Alternate between black and white blocks
            current_color = (
                0 if ((i // block_size) + (j // block_size)) % 2 == 0 else 255
            )
            checkboard[i : i + block_size, j : j + block_size] = current_color

    noise = generate_noise(size)

    composite = np.uint8(checkboard + (noise * 0.01))

    print(f'Check: {checkboard[0][0]} Noise: {noise[0][0]} sum: {composite[0][0]}')

    return composite


def generate_input_files():
    """
    Generates the input files

    """
    if not os.path.exists(INPUT_FILES_PATH):
        print("Input files directory does not exist, creating it...")
        os.mkdir(INPUT_FILES_PATH)

    pattern = generate_check_board()

    with open(IMAGE_INPUT_PATH, "wb") as f:
        f.write(pattern.tobytes())

    print(f"First byte: {pattern[0, 0]} Last byte: {pattern[-1, -1]}")

    return IMAGE_INPUT_PATH
