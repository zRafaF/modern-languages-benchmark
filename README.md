# Modern languages benchmark

This repository is made to compare some benchmarks of the languages `Rust`, `Go` and `Zig`.

It aims to provide a quick comparison of their relative performances on some use cases.

## Benchmarks

This repository implements the following benchmarks:

- Bubble sort

## Commands

### Install requirements

```bash
make install
```

### Build all languages

```bash
make build
```

### Generate input files

```bash
make generate
```

### Run benchmark on every language

```bash
make run
```

### Run benchmark on specific language

```bash
make run-rust
```

```bash
make run-go
```

```bash
make run-zig
```

### Specify number of iterations

```bash
make run ITERATIONS=1000
```

> Defaults to 10

## Extra

For more specific info, such as how to run, dependencies and so on, you can checkout the `README.md` on each directory.
