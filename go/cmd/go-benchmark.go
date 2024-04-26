package main

import (
	"encoding/binary"
	"fmt"
	"go-benchmark/pkg/bubblesort"
	"go-benchmark/pkg/gaussianblur"
	"os"
	"strconv"
)

type BenchmarkType byte

const (
	BubbleSort             BenchmarkType = 1
	GaussianBlurSequential BenchmarkType = 2
	GaussianBlurParallel   BenchmarkType = 3
)

// Save binary data to a file
func saveToFile(data []byte, filename string) error {
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	err = binary.Write(f, binary.LittleEndian, data)
	if err != nil {
		return err
	}
	return err
}

func main() {
	fmt.Println("Args n°:", len(os.Args))
	if len(os.Args) < 3 {
		fmt.Println("Error: Not enough arguments\nUsage: go run go-benchmark.go <image-path> <benchmark-type>\nbenchmark-type: (1=Bubble Sort) (2=Gaussian Blur Sequential) (3=Gaussian Blur Parallel)")
		os.Exit(1)
	}
	imagePath := os.Args[1]
	benchmarkType, err := strconv.Atoi(os.Args[2])

	if err != nil {
		fmt.Println("Error: Invalid benchmark type")
		os.Exit(1)
	}

	if imagePath == "" {
		fmt.Println("Error: No image path specified")
		os.Exit(1)
	}

	fmt.Println("Loading image from", imagePath)

	data, err := os.ReadFile(imagePath)
	if err != nil {
		fmt.Println("Error reading file:", err)
		os.Exit(1)
	}

	switch BenchmarkType(benchmarkType) {
	case BubbleSort:
		res := bubblesort.Sort(data)
		saveToFile(res, "go_result.raw")
	case GaussianBlurSequential:
		res := gaussianblur.Sequential(data)
		saveToFile(res, "go_result.raw")
	case GaussianBlurParallel:
		res := gaussianblur.Parallel(data)
		saveToFile(res, "go_result.raw")

	}

}
