## Receives a path to a .raw file with an array with values from [0 - 255] and plots it as an image

from matplotlib import pyplot as plt
import numpy as np

from input_generator import IMAGE_INPUT_PATH


def plot_image_from_raw_file(file_path: str):
    fig, axs = plt.subplots(1, 2)
    fig.suptitle("Image from raw file and input file")
    with open(IMAGE_INPUT_PATH, "rb") as file:
        data = file.read()
        data = np.frombuffer(data, dtype=np.uint8)
        data = data.reshape((256, 256))
        axs[0].imshow(
            data,
            cmap="gray",
        )
        axs[0].set_title("Input file")

    with open(file_path, "rb") as file:
        data = file.read()
        data = np.frombuffer(data, dtype=np.uint8)
        data = data.reshape((256, 256))
        axs[1].imshow(
            data,
            cmap="gray",
        )
        axs[1].set_title("Output file")

    plt.show()
