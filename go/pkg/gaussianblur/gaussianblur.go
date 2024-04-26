package gaussianblur

import (
	"math"
)

func index(x, y, sideSize int) int {
	return x*sideSize + y
}

func applyKernel(data []byte, kernel [][]float64, kernelSum float64, x, y, sideSize int) byte {
	sum := 0.0
	kSize := len(kernel)
	kHalf := kSize / 2
	for i := -kHalf; i <= kHalf; i++ {
		for j := -kHalf; j <= kHalf; j++ {
			nx, ny := x+i, y+j
			if nx >= 0 && nx < sideSize && ny >= 0 && ny < sideSize {
				sum += float64(data[index(nx, ny, sideSize)]) * kernel[i+kHalf][j+kHalf]
			}
		}
	}
	return byte(math.Round(sum / kernelSum))
}

// applyConvolution applies a convolution to the data using the given kernel.
func applyConvolution(data []byte, kernel [][]float64, kernelSum float64, sideSize int) []byte {
	result := make([]byte, len(data))
	for x := 0; x < sideSize; x++ {
		for y := 0; y < sideSize; y++ {
			result[index(x, y, sideSize)] = applyKernel(data, kernel, kernelSum, x, y, sideSize)
		}
	}
	return result
}

func generateGaussianKernel(size int, sigma float64) ([][]float64, float64) {
	// Initialize the kernel
	kernel := make([][]float64, size)
	for i := range kernel {
		kernel[i] = make([]float64, size)
	}

	// Calculate the center point of the kernel
	center := size / 2

	// Total sum of all elements for normalization
	total := 0.0

	// Compute the kernel values
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			x := float64(i - center)
			y := float64(j - center)
			kernel[i][j] = (1.0 / (2 * math.Pi * sigma * sigma)) * math.Exp(-(x*x+y*y)/(2*sigma*sigma))
			total += kernel[i][j]
		}
	}

	// Normalize the kernel so that the sum of all elements is 1
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			kernel[i][j] /= total
		}
	}

	return kernel, total
}

/*
 * Receives an array of bytes and applies a Gaussian blur to it.
 */
func Sequential(arr []byte) []byte {
	kernel, kernelSum := generateGaussianKernel(3, 2)

	sideSize := int(math.Sqrt(float64(len(arr))))

	// Apply convolution using the Gaussian kernel
	return applyConvolution(arr, kernel, kernelSum, sideSize)
}

/*
 * Receives an array of bytes and applies a Gaussian blur to it.
 */
func Parallel(arr []byte) []byte {

	return arr
}
