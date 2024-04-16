package bubblesort

func Sort(arr []byte) []byte {
	len := len(arr)

	swapped := true
	for i := 0; i < len && swapped; i++ {
		swapped = false
		for j := 0; j < len-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				swapped = true
			}
		}
	}
	return arr
}
