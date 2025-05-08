from PIL import Image

# Define matrix value constants
WHITE = 1
BLACK = 2
SPECIAL_BLACK = 3
# Note: We remove value 0 (gray) from final output to keep it scannable.

def create_qr_image(matrix, module_size=10, quiet_zone=4):
    """
    Create a scannable QR code image from the matrix.

    :param matrix: 2D list where:
        - 1 = white module
        - 2 = black module
        - 3 = reserved/special black module
    :param module_size: Pixel size for each module
    :param quiet_zone: Width of white border around the QR code (in modules)
    :return: PIL.Image object
    """
    qr_size = len(matrix)
    total_size = (qr_size + 2 * quiet_zone) * module_size
    img = Image.new('RGB', (total_size, total_size), color=(255, 255, 255))  # full white background

    for y in range(qr_size):
        for x in range(qr_size):
            value = matrix[y][x]

            # Only process known values (1 = white, 2/3 = black)
            if value == WHITE:
                color = (255, 255, 255)  # white
            elif value in (BLACK, SPECIAL_BLACK):
                color = (0, 0, 0)        # black
            else:
                continue  # Skip or treat unknowns as white (ensures scannability)

            # Calculate pixel position with quiet zone offset
            top_left_x = (x + quiet_zone) * module_size
            top_left_y = (y + quiet_zone) * module_size

            # Fill square block
            for dy in range(module_size):
                for dx in range(module_size):
                    img.putpixel((top_left_x + dx, top_left_y + dy), color)

    return img
