package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <path_to_raw_image>")
		os.Exit(1)
	}
	// Get the path to the .raw image file from command line argument
	imagePath := os.Args[1]

	fmt.Println("Loading image from", imagePath)

	// Open the .raw image file
	file, err := os.Open(imagePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		os.Exit(1)
	}
	defer file.Close()

	// Get the file size
	fileInfo, err := file.Stat()
	if err != nil {
		fmt.Println("Error getting file information:", err)
		os.Exit(1)
	}
	fileSize := fileInfo.Size()

	// Read the contents of the file into a byte array
	imageData := make([]byte, fileSize)
	_, err = file.Read(imageData)
	if err != nil {
		fmt.Println("Error reading file:", err)
		os.Exit(1)
	}

	// Print the loaded image data
	fmt.Println(imageData)

}
