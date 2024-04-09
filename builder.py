import os


class Builder:
    def __init__(self, rust_directory, zig_directory, go_directory) -> None:
        self.rust_directory = rust_directory
        self.zig_directory = zig_directory
        self.go_directory = go_directory

    def get_portable_binary_name(self, binary_name: str) -> str:
        """
        Returns the portable binary name for the given binary name

        Args:
            binary_name (str): The binary name

        Returns:
            str: The portable binary name

        """
        return binary_name + ".exe" if os.name == "nt" else binary_name


    def build_rust_program(self):
        """
        Builds the Rust program and returns the path to the executable

        Returns:
            str: Path to the Rust executable

        """

        os.system(f"cd {self.rust_directory} && cargo build --release")

        return os.path.join(
            self.rust_directory, "target", "release", self.get_portable_binary_name("rust-benchmark")
        )


    def build_go_program(self):
        """
        Builds the Go program and returns the path to the executable

        Returns:
            str: Path to the Go executable

        """
        os.system(f"cd {self.go_directory} && make build")

        return os.path.join(self.go_directory, self.get_portable_binary_name("go-benchmark"))


    def build_zig_program(self):
        """
        Builds the Zig program and returns the path to the executable

        Returns:
            str: Path to the Zig executable

        """
        os.system(f"cd {self.zig_directory} && zig build")

        return os.path.join(
            self.zig_directory, "zig-out", "bin", self.get_portable_binary_name("zig-benchmark")
        )
