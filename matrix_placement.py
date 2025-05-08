import numpy as np
from image import create_qr_image 
import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def create_matrix(version):
    if version == 1:
        matrix = np.zeros((21,21))
    elif version == 2:
        matrix = np.zeros((25, 25))
    
    for row in matrix:
        print(row.tolist())
    add_finder_patterns(matrix,version)

    img = create_qr_image(matrix)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "qr_matrix_image.png")
    img.save(save_path)
    print(f"Image saved to: {save_path}")
    return matrix
    

def add_finder_patterns(matrix,version):
    if version == 1:
      print("This is a Version 1 matrix")
      for y in range(7):
        for x in range(7):
            # Draw black modules for the square border and center
            if (x in [0, 6] or y in [0, 6]) or (2 <= x <= 4 and 2 <= y <= 4):
                matrix[y][x] = 2  # black module
            else:
                matrix[y][x] = 1  # white module

      for y in range(7):
        for x in range(14, 21):
           if (x in [14, 20] or y in [0, 6]) or (16 <= x <= 18 and 2 <= y <= 4):
            matrix[y][x] = 2  
           else:
            matrix[y][x] = 1 

      for y in range(14, 21):
        for x in range(7):
         if (x in [0, 6] or y in [14, 20]) or (2 <= x <= 4 and 16 <= y <= 18):
            matrix[y][x] = 2  # black module
         else:
            matrix[y][x] = 1  # white module

    elif version == 2:
      print("this is a version 2 matrix!")
      for y in range(7):
        for x in range(7):
            if (x in [0, 6] or y in [0, 6]) or (2 <= x <= 4 and 2 <= y <= 4):
                matrix[y][x] = 2
            else:
                matrix[y][x] = 1

      for y in range(7):
        for x in range(18, 25):
            if (x in [18, 24] or y in [0, 6]) or (20 <= x <= 22 and 2 <= y <= 4):
                matrix[y][x] = 2
            else:
                matrix[y][x] = 1
      for y in range(18, 25):
        for x in range(7):
            if (x in [0, 6] or y in [18, 24]) or (2 <= x <= 4 and 20 <= y <= 22):
                matrix[y][x] = 2
            else:
                matrix[y][x] = 1

    print("with finder patterns")
    color_matrix(matrix)
    img = create_qr_image(matrix)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "qr_withfinderpatterns.png")
    img.save(save_path)
    print(f"Image saved to: {save_path}")
    add_separators(matrix,version)


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

def add_separators(matrix,version):
    """
    Corrected separators for 25x25 matrix (Version 2 QR Code).
    """
    if version == 1:
     for row in range(8):
      matrix[row][7] = 1
      matrix[7][row] = 1
      matrix[row][13] = 1
      matrix[13][row] = 1

     for row in range(14,21):
       matrix[7][row] = 1
       matrix[row][7] = 1


    if version == 2: 
     for i in range(8):
        matrix[i][7] = 1
        matrix[7][i] = 1

     for i in range(8):
        matrix[i][17] = 1
     for i in range(18, 25):  
        matrix[7][i] = 1


     for i in range(8):
        matrix[17][i] = 1
     for i in range(18, 25):
        matrix[i][7] = 1

    print("with separators")
    color_matrix(matrix)
    img = create_qr_image(matrix)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "qr_with_seperators.png")
    img.save(save_path)
    print(f"Image saved to: {save_path}")

    if version == 2:
      add_alignment_patterns(matrix,version)
    elif version == 1:
      add_timing_patterns(matrix,version)
   

def add_timing_patterns(matrix,version):
    if version == 1:
     for i in range(8, 13):  # This should be range(8, matrix.shape[1]-8) for bigger versions
        matrix[6][i] = 2 if i % 2 == 0 else 1  # Alternating black (2) and white (1)
    
    # Vertical timing pattern (column 6)
     for i in range(8, 13):  # This should be range(8, matrix.shape[0]-8) for bigger versions
        matrix[i][6] = 2 if i % 2 == 0 else 1  # Alternating black (2) and white (1)

    if version == 2:
     for i in range(8, 25 - 8):
        matrix[6][i] = 2 if i % 2 == 0 else 1
        matrix[i][6] = 2 if i % 2 == 0 else 1

    print("with timing patterns")
    color_matrix(matrix)
    reserve_format_information(matrix,version)


def reserve_format_information(matrix,version):
    # Reserve format info areas
      # Place the dark module
    
    if version == 1:
     for row in range(0,9):
        matrix[row][8] = 3

     for row in range(0,8):
        matrix[8][row] = 3

     for row in range(13,21):
        matrix[row][8] = 3
     
     for row in range(13, 21):
       matrix[8][row] = 3

    elif version == 2:


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
   

def add_alignment_patterns(matrix,version):
    # For version 2, there is only one alignment pattern at (18,18)
    draw_alignment_pattern(matrix, 18, 18,version)

def draw_alignment_pattern(matrix, row, col,version):
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
    add_timing_patterns(matrix,version)


def place_data_bits_v1(matrix, bitstream):
    # List to store the coordinates of placed data bits
    data_bit_positions = []

    """
    Places the encoded data bits in the QR matrix.

    Data bits are placed starting at the bottom-right of the matrix,
    in 2-module vertical columns, moving up and down alternately.
    Reserved/function pattern modules (matrix[x][y] >= 1) are skipped.
    """
    # Convert bitstream from '0'/'1' to 1 (white), 2 (black)
    converted_bits = []
    for byte in bitstream:
        for bit in byte:
            converted_bits.append(1 if bit == '0' else 2)

    size = len(matrix)
    direction_up = True  # start moving upward
    y = size - 1 if size % 2 == 1 else size - 2  # rightmost column (even index)

    while y > 0 and converted_bits:
        x = size - 1 if direction_up else 0

        while (0 <= x < size) and converted_bits:
            for dx in [0, -1]:  # current column and the one left to it
                col = y + dx
                if 0 <= col < size:
                    if matrix[x][col] == 0:  # Check if the position is empty
                        matrix[x][col] = converted_bits.pop(0)
                        data_bit_positions.append((x, col))  # Capture the coordinate

            # Move up or down depending on direction
            x = x - 1 if direction_up else x + 1

        # Change direction and move 2 columns left
        direction_up = not direction_up
        y -= 2  # next 2-module column

        # Skip vertical timing pattern (usually column 6)
        if y == 6:
            y -= 1

    # Print matrix and the captured coordinates of the placed data bits
    print("after data bits")
    print(matrix)
    return matrix, data_bit_positions
       
def place_data_bits_v2(matrix, bitstream):
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

    for row in range(size):
     for col in range(size):
        if matrix[row][col] == 0:
            matrix[row][col] = 1  # Fill empty spots with white

     
    print("after data bits")
    color_matrix(matrix)
    return matrix, data_bit_positions


def apply_mask_0(matrix, data_bit_positions):
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

def evaluation_condition_1(matrix):
    """
    Check each row and each column for sequences of 5 or more consecutive modules 
    of the same color. Apply penalties as described.
    """
    penalty = 0
    size = len(matrix)

    for row in matrix:
        count = 1
        previous = row[0]
        for j in range(1, size):
            if row[j] == previous:
                count += 1
            else:
                if count >= 5:
                    penalty += 3 + (count - 5)
                count = 1
                previous = row[j]
        if count >= 5:
            penalty += 3 + (count - 5)

    for col in range(size):
        count = 1
        previous = matrix[0][col]
        for i in range(1, size):
            if matrix[i][col] == previous:
                count += 1
            else:
                if count >= 5:
                    penalty += 3 + (count - 5)
                count = 1
                previous = matrix[i][col]
        if count >= 5:
            penalty += 3 + (count - 5)

    print(f"Penalty from Condition 1: {penalty}")
    return penalty


def evaluation_condition_2(matrix):
    """
    Evaluate penalty condition 2:
    Look for 2x2 blocks (or larger) of same-colored modules.
    Add 3 penalty points for each 2x2 block found.
    """
    penalty = 0
    size = len(matrix)
    for row in range(size - 1):
        for col in range(size - 1):
            # Check 2x2 block starting at (row, col)
            color = matrix[row][col]
            if (matrix[row][col+1] == color and
                matrix[row+1][col] == color and
                matrix[row+1][col+1] == color):
                penalty += 3

    print(f"Penalty from Condition 2: {penalty}")
    return penalty

def evaluation_condition_3(matrix):
    """
    Penalty Condition 3:
    Look for the patterns 2 1 2 2 2 1 2 1 1 1 1 or 1 1 1 1 2 1 2 2 2 1 2
    in both rows and columns. Each occurrence adds 40 points.
    """
    penalty = 0
    size = len(matrix)

    # Define the two forbidden patterns
    patterns = [
        [2,1,2,2,2,1,2,1,1,1,1],
        [1,1,1,1,2,1,2,2,2,1,2]
    ]

    # Check each row
    for r in range(size):
        row = matrix[r]
        for c in range(size - 11 + 1):
            segment = row[c:c+11]
            if any(np.array_equal(segment, p) for p in patterns):
                penalty += 40

    # Check each column
    for c in range(size):
        for r in range(size - 11 + 1):
            segment = [matrix[r+i][c] for i in range(11)]
            if any(np.array_equal(segment, p) for p in patterns):
                penalty += 40

    print(f"Penalty from Condition 3: {penalty}")
    return penalty

def evaluation_condition_4(matrix):
    """
    The Final evaluation condition is based on the ratio of light modules to dark modules to calculate this penalty rule.
    """
    num_of_modules = 0
    dark_modules = 0
    
    # Count the total number of modules in the matrix
    for row in matrix:
        num_of_modules += len(row)
    
    # Count the dark modules (assuming dark modules are represented by 2)
    dark_modules = np.sum(matrix == 2)

    print("Total number of modules in the matrix:", num_of_modules)
    print("Number of dark modules:", dark_modules)

    # Calculate the percentage of dark modules
    dark_percent = (dark_modules / num_of_modules) * 100
    print("Percentage of modules in the matrix that are dark:", dark_percent)

    # Step 4: Determine the previous and next multiples of 5
    prev_multiple_of_5 = (dark_percent // 5) * 5
    next_multiple_of_5 = prev_multiple_of_5 + 5 if dark_percent % 5 != 0 else prev_multiple_of_5
    
    print("Previous multiple of 5:", prev_multiple_of_5)
    print("Next multiple of 5:", next_multiple_of_5)

    # Step 5: Subtract 50 from each of these multiples of five and take absolute value
    prev_multiple_of_5 = abs(prev_multiple_of_5 - 50)
    next_multiple_of_5 = abs(next_multiple_of_5 - 50)
    
    print("After subtracting 50 and taking the absolute value:")
    print("Previous multiple of 5:", prev_multiple_of_5)
    print("Next multiple of 5:", next_multiple_of_5)

    # Step 6: Divide each by 5
    prev_multiple_of_5_divided = prev_multiple_of_5 / 5
    next_multiple_of_5_divided = next_multiple_of_5 / 5

    print("Divided by 5:")
    print("Previous multiple of 5:", prev_multiple_of_5_divided)
    print("Next multiple of 5:", next_multiple_of_5_divided)

    # Step 7: Take the smallest of the two numbers and multiply by 10
    penalty_score = min(prev_multiple_of_5_divided, next_multiple_of_5_divided) * 10

    print("Penalty score #4:", penalty_score)
    return penalty_score

def evaluate_penalty(matrix):
    score1 = evaluation_condition_1(matrix)
    score2 = evaluation_condition_2(matrix)
    score3 = evaluation_condition_3(matrix)
    score4 = evaluation_condition_4(matrix)
    total_penalty = score1 + score2 + score3 + score4
    print("total penalty : ", total_penalty)
    return total_penalty



def format_info(matrix,version,best_mask):
    if best_mask == 0:
       format_bits = "111011111000100"
    if best_mask == 1:
       format_bits = "111001011110011"
    if best_mask == 2:
       format_bits = "111110110101010"
    if best_mask == 3:
       format_bits = "111100010011101"
    if best_mask == 4:
       format_bits = "110011000101111"
    if best_mask == 5:
       format_bits = "110001100011000"
    if best_mask == 6:
       format_bits = "110110001000001"
    if best_mask == 7:
       format_bits = "110100101110110"
    
    def format_value(bit):
        return 2 if bit == '1' else 1
        # Place format bits 0–6 in column 8 from row 24 to 18
    
    if version == 1:
        matrix[20][8] = format_value(format_bits[0])
        matrix[19][8] = format_value(format_bits[1])
        matrix[18][8] = format_value(format_bits[2])
        matrix[17][8] = format_value(format_bits[3])
        matrix[16][8] = format_value(format_bits[4])
        matrix[15][8] = format_value(format_bits[5])
        matrix[14][8] = format_value(format_bits[6])

        matrix[8][0] = format_value(format_bits[0])
        matrix[8][1] = format_value(format_bits[1])
        matrix[8][2] = format_value(format_bits[2])
        matrix[8][3] = format_value(format_bits[3])
        matrix[8][4] = format_value(format_bits[4])
        matrix[8][5] = format_value(format_bits[5])
        matrix[8][7] = format_value(format_bits[6])
        matrix[8][8] = format_value(format_bits[7])

        matrix[7][8] = format_value(format_bits[8])
        matrix[5][8] = format_value(format_bits[9])
        matrix[4][8] = format_value(format_bits[10])
        matrix[3][8] = format_value(format_bits[11])
        matrix[2][8] = format_value(format_bits[12])
        matrix[1][8] = format_value(format_bits[13])
        matrix[0][8] = format_value(format_bits[14])

        matrix[8][13] = format_value(format_bits[7])
        matrix[8][14] = format_value(format_bits[8])
        matrix[8][15] = format_value(format_bits[9])
        matrix[8][16] = format_value(format_bits[10])
        matrix[8][17] = format_value(format_bits[11])
        matrix[8][18] = format_value(format_bits[12])
        matrix[8][19] = format_value(format_bits[13])
        matrix[8][20] = format_value(format_bits[14])



    elif version == 2:
     for i in range(7):  # i = 0 to 6
        row = 24 - i
        matrix[row][8] = format_value(format_bits[i])
   
   
     count = 0
     for i in range(6):
          matrix[8][i] = format_value(format_bits[count])
          count += 1
     matrix[8][7] = format_value(format_bits[6])
     matrix[8][8] = format_value(format_bits[7])
     matrix[7][8] = format_value(format_bits[8])

 
     count2 = 9
     for i in range(5, -1, -1):  # From 5 down to 0
       matrix[i][8] =  format_value(format_bits[count2])
       count2 += 1

     count3 = 7
     for i in range(17,25):
        matrix[8][i] =  format_value(format_bits[count3])
        count3 += 1

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 3:
                matrix[i][j] = 1


    print("after placing format bits")
    color_matrix(matrix)
    return matrix
