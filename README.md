# Modern languages benchmark

This repository is made to compare some benchmarks of the languages `Rust`, `Go` and `Zig`.

It aims to provide a quick comparison of their relative performances on some use cases.

## Benchmarks

This repository implements the following benchmarks:

- Bubble sort
- Single threaded blur
- Multi threaded blur

The data for the benchmarks is generated randomly and saved in a `.raw` file, which is then read by the programs.

## Commands

### Install requirements

```shell
make install
```

### Build all languages

```shell
make build
```

### Generate input files

```shell
make generate
```

### Run benchmark on every language

```shell
make run
```

### Run benchmark on specific language

```shell
make run-rust
```

```shell
make run-go
```

```shell
make run-zig
```

### Run fresh benchmark

Rebuilds the source code and re generates the input files

```shell
make run-fresh
```

```shell
make run-fresh-zig
```

```shell
make run-fresh-go
```

```shell
make run-fresh-rust
```

### Specify number of iterations

```shell
make run ITERATIONS=1000
```

> Defaults to 10
> Works on specific language commands and fresh as well

### Specify benchmark type

```shell
make run TYPE=1
```

- 1 - Bubble sort
- 2 - Single threaded blur
- 3 - Multi threaded blur

> Defaults to 1
> Works on specific language commands and fresh as well

### Show the output file as an image

```shell
make show-go
make show-zig
make show-rust
```

### Show input file as an image

```shell
make show-input
```

## Extra

For more specific info, such as how to run, dependencies and so on, you can checkout the `README.md` on each directory.
