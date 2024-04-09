import random
import os.path


VECTOR_INPUT_PATH = os.path.join("inputfiles","vector_input.txt")

def generate_sorting_vector_file():
    """
    Generates the vector file (File used as input for the benchmarks)

    """

    min_rand_number = 0
    max_rand_number = 1000

    if not os.path.exists("inputfiles"):
        os.mkdir("inputfiles")

    # creates a file named inputfiles/vector_input.txt and fills it with a vector with random numbers
    with open(VECTOR_INPUT_PATH, "w") as f:
        f.write(" ".join([str(random.randint(0, 1000)) for _ in range(100000)]))

    return
