import random

def generate_sorting_vector_file():
    """
    Generates the vector file (File used as input for the benchmarks)

    """
    # creates a file named inputfiles/vector_input.txt and fills it with a vector with random numbers
    with open("inputfiles/vector_input.txt", "w") as f:
        f.write(" ".join([str(random.randint(0, 1000)) for _ in range(100000)]))

    return
