package gaussianblur

import (
	"fmt"
	"math"
)

func uniToBiDimensional(arr []byte, sideSize int) [][]byte {
	bidimensional := make([][]byte, sideSize)
	for i := 0; i < sideSize; i++ {
		bidimensional[i] = make([]byte, sideSize)
		for j := 0; j < sideSize; j++ {
			bidimensional[i][j] = arr[i*sideSize+j]
		}
	}
	return bidimensional
}

/*
 * Receives an array of bytes and applies a Gaussian blur to it.
 */
func Sequential(arr []byte) []byte {
	sideSize := int(math.Sqrt(float64(len(arr))))
	arr2d := uniToBiDimensional(arr, sideSize)
	for i := 0; i < sideSize; i++ {
		for j := 0; j < sideSize; j++ {
			fmt.Print(arr2d[i][j], " ")
		}
		fmt.Println()
	}
	return arr
}

/*
 * Receives an array of bytes and applies a Gaussian blur to it.
 */
func Parallel(arr []byte) []byte {

	return arr
}
