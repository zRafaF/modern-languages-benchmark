package bubblesort

func Sort(arr []byte) []byte {
	len := len(arr)
	for {
		swapped := false
		for i := 0; i < len-1; i++ {
			if arr[i] > arr[i+1] {
				arr[i], arr[i+1] = arr[i+1], arr[i]
				swapped = true
			}
		}
		if !swapped {
			break
		}

	}
	return arr
}
