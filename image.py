import turtle
def create_qr_image(matrix, module_size=10, quiet_zone=4, color=(0, 0, 0)):
    """
    Create a scannable QR code image from the matrix.

    :param matrix: 2D list of QR values (1 = white, 2 = black, 3 = special black)
    :param module_size: Pixel size for each module
    :param quiet_zone: Border padding in modules
    :param color: RGB tuple for the dark modules (default black)
    :return: PIL.Image object
    """
    from PIL import Image

    WHITE = 1
    BLACK = 2
    SPECIAL_BLACK = 3

    qr_size = len(matrix)
    total_size = (qr_size + 2 * quiet_zone) * module_size
    img = Image.new('RGB', (total_size, total_size), color=(255, 255, 255))  # background is white

    for y in range(qr_size):
        for x in range(qr_size):
            value = matrix[y][x]

            if value == WHITE:
                fill_color = (255, 255, 255)  # white
            elif value in (BLACK, SPECIAL_BLACK):
                fill_color = color  # use selected color instead of black
            else:
                continue  # ignore unknowns

            top_left_x = (x + quiet_zone) * module_size
            top_left_y = (y + quiet_zone) * module_size

            for dy in range(module_size):
                for dx in range(module_size):
                    img.putpixel((top_left_x + dx, top_left_y + dy), fill_color)

    return img

def create_qr_image2(matrix, module_size=10, quiet_zone=8, color=(0, 0, 0)):
    from PIL import Image, ImageDraw

    WHITE = 1
    BLACK = 2
    SPECIAL_BLACK = 3

    qr_size = len(matrix)
    total_size = (qr_size + 2 * quiet_zone) * module_size

    # Transparent image (RGBA)
    img = Image.new('RGBA', (total_size, total_size), (255, 255, 255, 0))

    # Draw QR code
    for y in range(qr_size):
        for x in range(qr_size):
            value = matrix[y][x]

            if value == WHITE:
                fill_color = (255, 255, 255, 255)
            elif value in (BLACK, SPECIAL_BLACK):
                fill_color = (*color, 255)
            else:
                continue

            top_left_x = (x + quiet_zone) * module_size
            top_left_y = (y + quiet_zone) * module_size

            for dy in range(module_size):
                for dx in range(module_size):
                    img.putpixel((top_left_x + dx, top_left_y + dy), fill_color)
                    
    mask = Image.new('L', (total_size, total_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    center = total_size // 2
    radius = total_size // 2 - module_size
    draw_mask.ellipse((center - radius, center - radius, center + radius, center + radius), fill=255)

   
    img.putalpha(mask)

    draw = ImageDraw.Draw(img)
    draw.ellipse(
        (center - radius, center - radius, center + radius, center + radius),
        outline=(255, 255, 255, 255), width=module_size
    )
    draw.ellipse(
        (center - radius, center - radius, center + radius, center + radius),
        outline=(0, 0, 0, 255), width=1
    )

    return img

def create_qr_image3(matrix, module_size=10, quiet_zone=12, color=(0, 0, 0)):
    """
    Create a scannable QR code image from the matrix with a diamond-shaped white border,
    black outline, and transparent background outside the diamond.

    :param matrix: 2D list of QR values (1 = white, 2 = black, 3 = special black)
    :param module_size: Pixel size for each module
    :param quiet_zone: Border padding in modules
    :param color: RGB tuple for the dark modules (default black)
    :return: PIL.Image object with transparency
    """
    from PIL import Image, ImageDraw

    WHITE = 1
    BLACK = 2
    SPECIAL_BLACK = 3

    qr_size = len(matrix)
    total_size = (qr_size + 2 * quiet_zone) * module_size

    # Create transparent RGBA image
    img = Image.new('RGBA', (total_size, total_size), (255, 255, 255, 0))

    # Draw QR modules
    for y in range(qr_size):
        for x in range(qr_size):
            value = matrix[y][x]

            if value == WHITE:
                fill_color = (255, 255, 255, 255)
            elif value in (BLACK, SPECIAL_BLACK):
                fill_color = (*color, 255)
            else:
                continue

            top_left_x = (x + quiet_zone) * module_size
            top_left_y = (y + quiet_zone) * module_size

            for dy in range(module_size):
                for dx in range(module_size):
                    img.putpixel((top_left_x + dx, top_left_y + dy), fill_color)

    # Create diamond-shaped mask
    mask = Image.new('L', (total_size, total_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    center = total_size // 2
    radius = total_size // 2 - module_size

    # Define diamond (rhombus) corners
    diamond = [
        (center, center - radius),  # top
        (center + radius, center),  # right
        (center, center + radius),  # bottom
        (center - radius, center),  # left
    ]
    draw_mask.polygon(diamond, fill=255)

    # Apply mask to alpha channel
    img.putalpha(mask)

    # Draw white diamond border
    draw = ImageDraw.Draw(img)
    draw.polygon(diamond, outline=(255, 255, 255, 255), width=module_size)

    # Draw black outline on top
    draw.polygon(diamond, outline=(0, 0, 0, 255), width=1)

    return img
