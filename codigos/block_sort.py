def block_sort(arr):
    # Implementação simplificada do BlockSort
    n = len(arr)
    if n <= 1:
        return arr

    max_value = max(arr)
    min_value = min(arr)
    range_value = max_value - min_value + 1

    # Dividir o array em blocos
    num_blocks = int(n ** 0.5)
    block_size = (range_value + num_blocks - 1) // num_blocks

    # Criar e inicializar blocos
    blocks = [[] for _ in range(num_blocks)]
    for num in arr:
        block_index = (num - min_value) // block_size
        blocks[block_index].append(num)

    # Ordenar cada bloco e juntar os blocos
    sorted_array = []
    for block in blocks:
        sorted_array.extend(sorted(block))

    for i in range(n):
        arr[i] = sorted_array[i]
