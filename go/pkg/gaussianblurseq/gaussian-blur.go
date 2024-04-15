package gaussianblurseq

/*
 * Receives an array of integers and applies a Gaussian blur to it.
 */
func GaussianBlurSeq(arr []int) []int {
	for i := 1; i < len(arr)-1; i++ {
		arr[i] = (arr[i-1] + arr[i] + arr[i+1]) / 3
	}
	return arr
}
