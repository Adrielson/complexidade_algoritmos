def quick_sort_in_place(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        p = partition(arr, low, high)
        quick_sort(arr, low, p)
        quick_sort(arr, p + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[(low + high) // 2]
    i = low - 1
    j = high + 1
    
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        
        j -= 1
        while arr[j] > pivot:
            j -= 1
        
        if i >= j:
            return j
        
        arr[i], arr[j] = arr[j], arr[i]
