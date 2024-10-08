import glob
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# retrieves the latest saved file on the disk
def get_latest_file(dir):
    """
    Retrieve the most recently modified file from a directory.

    Parameters:
    dir (str): The directory path where files are stored.

    Returns:
    str: The path to the latest file.
    """
    list_of_files = glob.glob(f"{dir}/*")
    latest_file = max(list_of_files, key=os.path.getmtime)

    return latest_file


def replace_rgb(image, old_rgb, new_rgb):
    """
    Replace all instances of a specific RGB color in an image with a new RGB color.

    Parameters:
    image (PIL.Image): The input image.
    old_rgb (tuple): The RGB color to be replaced (r1, g1, b1).
    new_rgb (tuple): The new RGB color to replace the old one (r2, g2, b2).

    Returns:
    PIL.Image: The modified image with the replaced colors.
    """
    img_array = np.array(image)

    r1, g1, b1 = old_rgb
    r2, g2, b2 = new_rgb

    red, green, blue = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    img_array[:, :, :3][mask] = [r2, g2, b2]

    return Image.fromarray(img_array)


def paste_image(img, posn, dst):
    """
    Paste an image onto a destination image at the specified position.

    Parameters:
    img (PIL.Image): The image to be pasted.
    posn (tuple): The position (x, y) where the image will be pasted.
    dst (PIL.Image): The destination image where the image will be pasted.

    Returns:
    None
    """
    # needed to correctly paste images with alpha
    image = img.load()
    width, height = img.size
    dst_img = dst.load()

    for y in range(height):
        for x in range(width):
            if image[x, y] != (0, 0, 0, 0):
                try:
                    dst_img[x + posn[0], y + posn[1]] = image[x, y]
                except IndexError:
                    pass


def centered_pos(pos1, pos2):
    """
    Calculate the centered position of one image relative to another.

    Parameters:
    pos1 (PIL.Image): The larger image.
    pos2 (PIL.Image): The smaller image to be centered within the larger one.

    Returns:
    tuple: The (x, y) coordinates for centering the smaller image.
    """
    W, H = pos1.size
    w, h = pos2.size

    return (int((W - w) / 2), int((H - h) / 2))


def draw_rectangle(image, rgb, top_left, bot_right):
    """
    Draw a filled rectangle on an image.

    Parameters:
    image (PIL.Image): The image on which to draw.
    rgb (tuple): The RGBA color to fill the rectangle.
    top_left (tuple): The top-left corner of the rectangle.
    bot_right (tuple): The bottom-right corner of the rectangle.

    Returns:
    PIL.Image: The image with the drawn rectangle.
    """
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((top_left, bot_right), fill=(rgb))

    return image


def draw_text(
    image,
    text,
    rgb,
    font_dir,
    font_size,
    bot_right,
    center_text=False,
    anchor="lt",
    nickname=False,
):
    """
    Draw text on an image, with optional resizing for nicknames and centering.

    Parameters:
    image (PIL.Image): The image on which to draw the text.
    text (str): The text to be drawn.
    rgb (tuple): The RGB color of the text.
    font_size (int): The font size for the text.
    bot_right (tuple): The position for the text (bottom-right corner).
    center_text (bool, optional): If True, the text will be centered. Defaults to False.
    anchor (str, optional): Text anchor point. Defaults to "lt" (left-top).
    nickname (bool, optional): If True, the text will automatically resize if it's a nickname. Defaults to False.

    Returns:
    None
    """
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.truetype(font_dir.as_posix(), font_size)

    # properly handles nickname resizing
    if nickname:
        nickname_w = ImageDraw.Draw(image).textbbox((0, 0), str(text), font=font)[2]
        image_w = image.size[0]
        margin = 10

        # if nickname is bigger than its slot, reduce font size until it fits
        while nickname_w > image_w - margin:
            font_size -= 1
            font = ImageFont.truetype(font_dir.as_posix(), font_size)
            nickname_w = ImageDraw.Draw(image).textbbox((0, 0), str(text), font=font)[2]

    if center_text:
        W, H = bot_right
        _, _, w, h = ImageDraw.Draw(image).textbbox((0, 0), str(text), font=font)

        draw.text(((W - w) / 2, (H - h) / 2), str(text), fill=rgb, font=font)
    else:
        draw.text(
            (bot_right[0], bot_right[1]), str(text), fill=rgb, font=font, anchor=anchor
        )


def open_image(input_file, size=(0, 0)):
    """
    Open an image file and resize it if specified.

    Parameters:
    input_file (str): The path to the input image file.
    size (tuple, optional): The new size (width, height) to resize the image. Defaults to (0, 0) (no resize).

    Returns:
    PIL.Image: The opened image.
    """
    try:
        image = Image.open(input_file)
    except FileNotFoundError:
        print(
            "FileNotFoundError: please check your input file and try again.\n"
            rf"Current input file: {input_file}"
        )
        sys.exit(1)

    if size != (0, 0):
        image.resize(
            (size[0], size[1]),
            resample=Image.BOX,
        )

    return image
