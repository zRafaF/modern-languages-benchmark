package boxblur

import (
	"math"
	"sync"
)

func index(x, y, sideSize int) int {
	return x*sideSize + y
}

func indexTo2d(idx, sideSize int) (int, int) {
	return idx / sideSize, idx % sideSize
}

func generateBoxBlurKernel(size int) []float64 {
	kernel := make([]float64, size*size)
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			kernel[index(i, j, size)] = (1.0 / float64(size*size))
		}
	}
	return kernel
}

func applyConvolution(arr []byte, arraySize int, elementIdx int, kernel []float64, kernelSize int) byte {
	var sum float64
	for i := 0; i < kernelSize; i++ {
		for j := 0; j < kernelSize; j++ {
			x, y := indexTo2d(elementIdx, arraySize)
			x += i - kernelSize/2
			y += j - kernelSize/2
			if x < 0 || y < 0 || x >= arraySize || y >= arraySize {
				continue
			}
			sum += float64(arr[index(x, y, arraySize)]) * kernel[index(i, j, kernelSize)]
		}
	}
	return byte(sum)

}

/*
 * Receives an array of bytes and applies a Box blur to it.
 */
func Sequential(arr []byte) []byte {
	const kernelSize = 19
	arraySize := int(math.Sqrt(float64(len(arr))))

	kernel := generateBoxBlurKernel(kernelSize)

	for idx, _ := range arr {
		arr[idx] = applyConvolution(arr, arraySize, idx, kernel, kernelSize)
	}

	return arr
}

/*
 * Receives an array of bytes and applies a Box blur to it.
 */
func Parallel(arr []byte) []byte {
	const kernelSize = 19
	kernel := generateBoxBlurKernel(kernelSize)
	arraySize := int(math.Sqrt(float64(len(arr))))
	numElements := len(arr)

	var wg sync.WaitGroup
	wg.Add(numElements)

	// Channel to receive results from goroutines
	resultCh := make(chan struct {
		idx int
		val byte
	}, numElements)

	// Launch goroutines for applying convolution to each element
	for idx := range arr {
		go func(elementIdx int) {
			defer wg.Done()
			val := applyConvolution(arr, arraySize, elementIdx, kernel, kernelSize)
			resultCh <- struct {
				idx int
				val byte
			}{elementIdx, val}
		}(idx)
	}

	// Close the result channel after all goroutines finish
	go func() {
		wg.Wait()
		close(resultCh)
	}()

	// Collect results from the channel and update the array
	for res := range resultCh {
		arr[res.idx] = res.val
	}

	// Apply convolution using the Gaussian kernel
	return arr
}
