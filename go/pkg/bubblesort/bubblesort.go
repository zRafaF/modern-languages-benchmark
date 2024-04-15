package bubblesort

func Sort(arr []byte) []byte {
	len := len(arr)

	for i := 0; i < len; i++ {
		for j := 0; j < len-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}

	return arr
}
