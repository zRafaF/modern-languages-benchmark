package main

import (
	"fmt"
	"os"
)

func main() {
	imagePath := os.Args[0]

	if imagePath == "" {
		fmt.Println("Error: No image path specified")
		os.Exit(1)
	}

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

	// buffer := bytes.NewBuffer(imageData)
	// var nowVar uint8
	// binary.Read(buffer, binary.BigEndian, &nowVar)
	// fmt.Println(nowVar)
	// // Print the loaded image data
	// data := binary.BigEndian.Uint16(imageData)
	// fmt.Println(data)

	// bubblesort.Sort(imageData)

	fmt.Println("Image loaded successfully")
}
