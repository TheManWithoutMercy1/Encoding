def apply_mask_1(matrix, data_bit_positions):
    # Mask condition: (row % 2) == 0
    for (x, y) in data_bit_positions:
        if (x % 2) == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern 1")
    return matrix

def apply_mask_2(matrix,data_bit_positions):
    # (column) mod 3 == 0
    for (x,y) in data_bit_positions:
        if (y) % 3 == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern 2")
    return matrix

def apply_mask_3(matrix,data_bit_positions):
   # (row + column) mod 3 == 0
   for (x,y) in data_bit_positions:
       if (x + y) % 3 == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

   print("after applying mask pattern 3")
   return matrix

def apply_mask_4(matrix, data_bit_positions):
    # Mask pattern 4: (floor(row / 2) + floor(column / 3)) mod 2 == 0
    for (x, y) in data_bit_positions:
        if ((x // 2) + (y // 3)) % 2 == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern 4")
    return matrix

def apply_mask_5(matrix, data_bit_positions):
    # Mask pattern 5: ((row * column) mod 2) + ((row * column) mod 3) == 0
    for (x, y) in data_bit_positions:
        product = x * y
        if (product % 2 + product % 3) == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern 5")
    return matrix

def apply_mask_6(matrix, data_bit_positions):
    # Mask pattern 6: (((row * column) mod 2) + ((row * column) mod 3)) mod 2 == 0
    for (x, y) in data_bit_positions:
        product = x * y
        if ((product % 2 + product % 3) % 2) == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern 6")
    return matrix


def apply_mask_7(matrix, data_bit_positions):
    # Mask pattern 7: (((row + column) mod 2) + ((row * column) mod 3)) mod 2 == 0
    for (x, y) in data_bit_positions:
        if (((x + y) % 2 + (x * y) % 3) % 2) == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern 7")
    return matrix
