import os


class Builder:
    def __init__(self, rust_directory, zig_directory, go_directory):
        """
        Initializes the Builder class

        Args:
            rust_directory (str): The Rust directory
            zig_directory (str): The Zig directory
            go_directory (str): The Go directory
        """
        self._rust_directory = rust_directory
        self._zig_directory = zig_directory
        self._go_directory = go_directory

        self.rust_build_path = os.path.join(
            self._rust_directory,
            "target",
            "release",
            self._get_portable_binary_name("rust-benchmark"),
        )
        self.go_build_path = os.path.join(
            self._go_directory, self._get_portable_binary_name("go-benchmark")
        )
        self.zig_build_path = os.path.join(
            self._zig_directory,
            "zig-out",
            "bin",
            self._get_portable_binary_name("zig-benchmark"),
        )

    def _get_portable_binary_name(self, binary_name: str) -> str:
        """
        Returns the portable binary name for the given binary name

        Args:
            binary_name (str): The binary name

        Returns:
            str: The portable binary name

        """
        return binary_name + ".exe" if os.name == "nt" else binary_name

    def _build_rust_program(self):
        """
        Builds the Rust program and returns the path to the executable

        Returns:
            str: Path to the Rust executable

        """

        os.system(f"cd {self._rust_directory} && cargo build --release")

        return self.rust_build_path

    def _build_go_program(self):
        """
        Builds the Go program and returns the path to the executable

        Returns:
            str: Path to the Go executable

        """
        os.system(f"cd {self._go_directory} && make build")

        return self.go_build_path

    def _build_zig_program(self):
        """
        Builds the Zig program and returns the path to the executable

        Returns:
            str: Path to the Zig executable

        """
        os.system(f"cd {self._zig_directory} && zig build")

        return self.zig_build_path

    def build_all_programs(self):
        """
        Builds all the programs

        """
        self._build_rust_program()
        self._build_go_program()
        self._build_zig_program()

    def does_builds_exist(
        self,
    ) -> bool:
        """
        Checks if the build exists

        Args:
            path (str): The path to the build

        Returns:
            bool: True if the build exists, False otherwise

        """
        # Check if all the build paths exist
        return all(
            [
                os.path.exists(self.rust_build_path),
                os.path.exists(self.go_build_path),
                os.path.exists(self.zig_build_path),
            ]
        )
