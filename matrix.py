import numpy as np
from image import create_qr_image 
import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def create_matrix():
    matrix = np.zeros((25, 25))
    for row in matrix:
        print(row.tolist())
    add_finder_patterns(matrix)
    return matrix

def add_finder_patterns(matrix):
    # Top-left finder pattern
    for y in range(7):
        for x in range(7):
            if (x in [0, 6] or y in [0, 6]) or (2 <= x <= 4 and 2 <= y <= 4):
                matrix[y][x] = 2
            else:
                matrix[y][x] = 1

    # Top-right finder pattern
    for y in range(7):
        for x in range(18, 25):
            if (x in [18, 24] or y in [0, 6]) or (20 <= x <= 22 and 2 <= y <= 4):
                matrix[y][x] = 2
            else:
                matrix[y][x] = 1

    # Bottom-left finder pattern
    for y in range(18, 25):
        for x in range(7):
            if (x in [0, 6] or y in [18, 24]) or (2 <= x <= 4 and 20 <= y <= 22):
                matrix[y][x] = 2
            else:
                matrix[y][x] = 1

    print("with finder patterns")
    color_matrix(matrix)
    add_separators(matrix)


def color_matrix(matrix):
    # Convert 0.0, 1.0, 2.0, etc. to integers (0, 1, 2, ...)
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            matrix[y][x] = int(matrix[y][x])  # Convert float to integer

    # Print matrix with colors (using terminal ANSI codes for simplicity)
    print("Matrix with colored 1s, 2s, and 3s:")
    for row in matrix:
        colored_row = ""
        for value in row:
            if value == 0:
                colored_row += "\033[0m 0 "  # Default color for 0
            elif value == 1:
                colored_row += "\033[94m 1 "  # Blue for 1
            elif value == 2:
                colored_row += "\033[92m 2 "  # Green for 2
            elif value == 3:
                colored_row += "\033[93m 3 "  # Yellow for 3
            else:
                colored_row += f"{value} "  # Default for other values
        print(colored_row + "\033[0m")  # Reset color after the row

def add_separators(matrix):
    """
    Corrected separators for 25x25 matrix (Version 2 QR Code).
    """

    # Top-left finder pattern separator
    for i in range(8):
        matrix[i][7] = 1
        matrix[7][i] = 1

    # Top-right finder pattern separator
    for i in range(8):
        matrix[i][17] = 1
    for i in range(18, 25):  # from 18 to 24
        matrix[7][i] = 1

    # Bottom-left finder pattern separator
    for i in range(8):
        matrix[17][i] = 1
    for i in range(18, 25):
        matrix[i][7] = 1

    print("with separators")
    color_matrix(matrix)
    add_alignment_patterns(matrix)
   

def add_timing_patterns(matrix):
    for i in range(8, 25 - 8):
        matrix[6][i] = 2 if i % 2 == 0 else 1
        matrix[i][6] = 2 if i % 2 == 0 else 1

    print("with timing patterns")
    color_matrix(matrix)
    reserve_format_information(matrix)


def reserve_format_information(matrix):
    # Reserve format info areas
      # Place the dark module
    matrix[17][8] = 2
    for i in range(18,25):
        matrix[i][8] = 3
    for i in range(6):
       matrix[8][i] = 3
    matrix[8][7] = 3
    matrix[8][8] = 3

    for i in range(6):
      matrix[i][8] = 3
    matrix[7][8] = 3
    matrix[8][8] = 3
    
    for i in range(17,25):
      matrix[8][i] = 3

    print("with reserved format info")
    color_matrix(matrix)
   # add_alignment_patterns(matrix)  # Now add alignment patterns

def add_alignment_patterns(matrix):
    # For version 2, there is only one alignment pattern at (18,18)
    draw_alignment_pattern(matrix, 18, 18)

def draw_alignment_pattern(matrix, row, col):
    """
    Draw a 5x5 alignment pattern centered at (row, col)
    """
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) == 2 or abs(dy) == 2:
                matrix[row + dy][col + dx] = 2  # Black border
            elif dx == 0 and dy == 0:
                matrix[row][col] = 2  # Center black dot
            else:
                matrix[row + dy][col + dx] = 1  # White inner

    print("with alignment patterns:")
    color_matrix(matrix)
    add_timing_patterns(matrix)

def place_data_bits(matrix, bitstream):
    data_bit_positions = []
    converted_bits = []

    for byte in bitstream:
        for bit in byte:
            converted_bits.append(1 if bit == '0' else 2)

    size = len(matrix)

    def try_place(row, col):
        if not converted_bits:
           print("no more data bits left!!1")
           return  # No more bits to place, just exit
        if matrix[row][col] == 0:  # Only place if it's 0
            matrix[row][col] = converted_bits.pop(0)
            data_bit_positions.append((row, col))

    print(bitstream)
    print(converted_bits)
    
    for row in range(24, 8, -1):  
        try_place(row, 24)
        try_place(row, 23)

    for row in range(9, 25):  
        try_place(row, 22)
        try_place(row, 21)

    for row in range(24, 20, -1):
        try_place(row, 20)
        try_place(row, 19)

    for row in range(15, 8, -1):
        try_place(row, 20)
        try_place(row, 19)

    for row in range(9, 16):
        try_place(row, 18)
        try_place(row, 17)

    for row in range(21, 25):
        try_place(row, 18)
        try_place(row, 17)

    for row in range(24, 20, -1):
        try_place(row, 16)
        try_place(row, 15)

    try_place(20, 15)
    try_place(19, 15)
    try_place(18, 15)
    try_place(17, 15)
    try_place(16, 15)

    for row in range(15, 6, -1):
        try_place(row, 16)
        try_place(row, 15)

    for row in range(5, -1, -1):
        try_place(row, 16)
        try_place(row, 15)

    for row in range(0, 6):
        try_place(row, 14)
        try_place(row, 13)

    for row in range(7, 25):
        try_place(row, 14)
        try_place(row, 13)

    for row in range(24, 6, -1):
        try_place(row, 12)
        try_place(row, 11)

    for row in range(5, -1, -1):
        try_place(row, 12)
        try_place(row, 11)

    for row in range(0, 6):
        try_place(row, 10)
        try_place(row, 9)

    for row in range(7, 25):
        try_place(row, 10)
        try_place(row, 9)

    for row in range(16, 8, -1):
        try_place(row, 8)
        try_place(row, 7)

    for row in range(9, 17):
        try_place(row, 5)
        try_place(row, 4)

    for row in range(16, 8, -1):
        try_place(row, 3)
        try_place(row, 2)

    for row in range(9,17):
         try_place(row, 1)
         try_place(row, 0)
     
    print("after data bits")
    color_matrix(matrix)
    return matrix, data_bit_positions


def apply_mask(matrix, data_bit_positions):
    # (row + column) mod 2 == 0
    for (x, y) in data_bit_positions:
        if (x + y) % 2 == 0:
            if matrix[x][y] == 1:
                matrix[x][y] = 2
            elif matrix[x][y] == 2:
                matrix[x][y] = 1

    print("after applying mask pattern zero")
    color_matrix(matrix)
    return matrix


def format_info(matrix):
    format_bits = "111011111000100"
    def format_value(bit):
        return 2 if bit == '1' else 1
        # Place format bits 0–6 in column 8 from row 24 to 18
    for i in range(7):  # i = 0 to 6
        row = 24 - i
        matrix[row][8] = format_value(format_bits[i])
   
   # for i in range(6)
    count = 0
    for i in range(6):
          matrix[8][i] = format_value(format_bits[count])
          count += 1
    matrix[8][7] = format_value(format_bits[6])
    matrix[8][8] = format_value(format_bits[7])
    matrix[7][8] = format_value(format_bits[8])

    #move from 5 to 1/0
    count2 = 9
    for i in range(5, -1, -1):  # From 5 down to 0
       matrix[i][8] =  format_value(format_bits[count2])
       count2 += 1

    count3 = 7
    for i in range(17,25):
        matrix[8][i] =  format_value(format_bits[count3])
        count3 += 1

    # Print matrix for debug
    print("after placing format bits")
    color_matrix(matrix)
    return matrix
