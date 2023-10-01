import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .draw_recolors import generate_recolor, get_latest_file, start_headless_driver
from .offsets import (
    char_offsets,
    portrait_multipliers,
    zoom_multipliers,
    nickname_multipliers,
)

file_dir = Path(os.path.dirname(os.path.realpath(__file__)))
char_dir = Path("static/Resources/Characters/Secondary")


# draws the standard layout
def draw_top8(
    nicknames: list,
    characters: list,
    skins: list,
    secondaries: list,
    tertiaries: list,
    resize_factor: float,
    layout_rgb: tuple = (255, 138, 132),
    bg_opacity: int = 100,
    save: bool = True,
) -> Image.Image:
    # layout settings (from last player to first player)
    placements = [1, 2, 3, 4, 5, 5, 7, 7]
    resizes = [1.223, 0.9, 0.9, 0.9, 0.675, 0.675, 0.675, 0.675]
    sizes = ["L", "M", "M", "M", "S", "S", "S", "S"]

    custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent / Path(
        "static/Resources/Characters/Main/Custom"
    )

    # checks for custom skins and returns a list of booleans
    skin_is_custom = [False for _ in range(len(skins))]
    for i in range(len(skins)):
        matched_pattern = re.search("([0-9a-fA-F]{4}-)*([0-9a-fA-F]{4})", skins[i])

        if matched_pattern:
            group = matched_pattern.group(0)
            skin_is_custom[i] = True if len(group) > 4 else False

    # only starts driver if any skin is custom, else sets driver to None
    if any(skin_is_custom):
        driver = start_headless_driver(custom_skins_dir)
    else:
        driver = None

    # creates portraits
    players = [
        draw_portrait(
            nicknames[i],
            characters[i],
            skins[i],
            placements[i],
            resizes[i],
            layout_rgb,
            sizes[i],
            custom_skins_dir,
            driver,
            secondaries[i],
            tertiaries[i],
            bg_opacity=bg_opacity,
            save=False,
            is_singles=True if isinstance(skins[0], str) else False,
        )
        for i in range(8)
    ]

    # creates output image
    output = Image.new(
        "RGBA", (players[0].size[0] + players[1].size[0] * 3 - 4, players[0].size[1])
    )

    paste_image(players[0], (0, 0), output)
    paste_image(players[1], (players[0].size[0] - 4, 0), output)
    paste_image(
        players[2], (players[0].size[0] + players[1].size[0] * 1 - 7, 0), output
    )
    paste_image(
        players[3], (players[0].size[0] + players[1].size[0] * 2 - 12, 0), output
    )
    paste_image(
        players[4],
        (players[0].size[0] + players[4].size[0] * 0 - 4, players[1].size[1]),
        output,
    )
    paste_image(
        players[5],
        (players[0].size[0] + players[4].size[0] * 1 - 8, players[1].size[1]),
        output,
    )
    paste_image(
        players[6],
        (players[0].size[0] + players[4].size[0] * 2 - 10, players[1].size[1]),
        output,
    )
    paste_image(
        players[7],
        (players[0].size[0] + players[4].size[0] * 3 - 12, players[1].size[1]),
        output,
    )

    # resizes the output image
    output = output.resize(
        (int(output.size[0] * resize_factor), int(output.size[1] * resize_factor)),
        resample=Image.BOX,
    )

    if save:
        output.save("output.png")

    return output


# draws an alternative layout
def draw_top8_columns(
    nicknames,
    characters,
    skins,
    secondaries,
    tertiaries,
    resize_factor,
    layout_rgb=(255, 138, 132),
    bg_opacity=100,
    save=True,
) -> Image.Image:
    # layout settings (from last player to first player)
    placements = [1, 2, 3, 4, 5, 5, 7, 7]
    resizes = [1 for _ in range(0, 8)]
    sizes = ["M" for _ in range(0, 8)]

    # creates portraits
    players = [
        draw_portrait(
            nicknames[i],
            characters[i],
            skins[i],
            placements[i],
            resizes[i],
            layout_rgb,
            sizes[i],
            secondaries[i],
            tertiaries[i],
            bg_opacity=bg_opacity,
            save=False,
        )
        for i in range(8)
    ]

    offset_x = 25
    offset_y = 25

    # creates output image
    output = Image.new(
        "RGBA",
        (
            players[0].size[0] * 4 + offset_x * 3,
            players[0].size[1] * 2 + offset_y * 1,
        ),
    )

    # draws layout
    for i in range(0, 4):
        paste_image(players[i], (players[i].size[0] * i + offset_x * i, 0), output)
        paste_image(
            players[i + 4],
            (players[i].size[0] * i + offset_x * i, players[i].size[1] + offset_y),
            output,
        )

    # resizes the output image
    output = output.resize(
        (int(output.size[0] * 1), int(output.size[1] * 1)),
        resample=Image.BOX,
    )

    if save:
        output.save("output.png")

    return output


def replace_rgb(image, old_rgb, new_rgb):
    img_array = np.array(image)

    r1, g1, b1 = old_rgb
    r2, g2, b2 = new_rgb

    red, green, blue = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    img_array[:, :, :3][mask] = [r2, g2, b2]

    return Image.fromarray(img_array)


def paste_image(img, posn, dst):
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
    W, H = pos1.size
    w, h = pos2.size

    return (int((W - w) / 2), int((H - h) / 2))


def draw_rectangle(image, rgb, top_left, bot_right):
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((top_left, bot_right), fill=(rgb))

    return image


def draw_text(
    image,
    text,
    rgb,
    font_size,
    bot_right,
    center_text=False,
    anchor="lt",
    nickname=False,
):
    font_dir = Path("static/Resources/Layout/Pixellari.ttf")
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.truetype(font_dir.as_posix(), font_size)

    # properly handles nickname resizing
    if nickname:
        # textsize was deprecated
        # nickname_w = draw.textsize(str(text), font)[0]

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
        # w, h = draw.textsize(str(text), font)
        _, _, w, h = ImageDraw.Draw(image).textbbox((0, 0), str(text), font=font)

        draw.text(((W - w) / 2, (H - h) / 2), str(text), fill=rgb, font=font)
    else:
        draw.text(
            (bot_right[0], bot_right[1]), str(text), fill=rgb, font=font, anchor=anchor
        )


def open_image(input_file, size=(0, 0)):
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


def draw_additional_char(character, portrait, position):
    input_file = Path(char_dir / f"{character}.png")

    if character != "None":
        try:
            secondary = Image.open(input_file)
            portrait.paste(secondary, position, secondary)
        except FileNotFoundError:
            print(
                "FileNotFoundError: please check your input file and try again.\n"
                rf"Current input file: {input_file}"
            )


def draw_portrait(
    nickname,
    characters,
    skins,
    placement,
    resizing,
    rgb,
    size,
    custom_skins_dir,
    driver,
    secondary=None,
    tertiary=None,
    bg_opacity=100,
    save=False,
    is_singles=True,
):
    # loads images
    layout = open_image(Path("static/Resources/Layout/char_portrait.png"))

    # creates new image to be used as background layer
    portrait = Image.new(
        "RGBA",
        (
            layout.size[0],
            int(layout.size[1] * portrait_multipliers[size]),
        ),
    )

    # creates opaque background behind the portrait
    draw_rectangle(portrait, (*rgb, bg_opacity), (0, 0), portrait.size)

    layout = layout.resize(
        (int(layout.size[0]), int(layout.size[1] * portrait_multipliers[size])),
        resample=Image.BOX,
    )

    # wraps parameters in list to handle singles tournaments
    if isinstance(skins[0], str):
        skins = [skins]
        characters = [characters]

    # flattens lists to handle doubles tournaments
    if isinstance(skins[0], list):
        skins = [item for sublist in skins for item in sublist]
        characters = [item for sublist in characters for item in sublist]

    for i, (character, skin) in enumerate(zip(characters, skins)):
        # needed to check for custom skins
        custom_skin = False

        try:
            matched_pattern = re.search("([0-9a-fA-F]{4}-)*([0-9a-fA-F]{4})", skin)

            if matched_pattern:
                matched_pattern = matched_pattern.group(0)

            if skin == matched_pattern:
                custom_skin = True

        except AttributeError:
            pass

        # returns character image file unless no character is requested
        if character:
            if not custom_skin:
                if character == "None":
                    char = Image.new("RGBA", (0, 0))
                else:
                    char_dir = Path(
                        f"static/Resources/Characters/Main/{character}/{skin}.png"
                    )
                    char = open_image(char_dir)
            else:
                # sets some useful directory variables
                custom_char_dir = Path(
                    custom_skins_dir / Path(character) / Path(f"{skin}.png")
                )

                # checks if custom skin already exists and uses it, acting as a caching mechanism
                if os.path.exists(custom_char_dir):
                    char = open_image(custom_char_dir)
                else:
                    # gets recolorer webpage
                    driver.get("https://readek.github.io/RoA-Skin-Recolorer/")

                    # create recolor of the requested character and skin code
                    generate_recolor(driver, character.title(), skin)

                    # gets latest created file and renames it
                    filename = get_latest_file(custom_skins_dir)

                    # tries to create custom skins folder for the specified character
                    try:
                        os.mkdir(Path(custom_skins_dir) / Path(character))
                    except FileExistsError:
                        pass

                    shutil.move(
                        filename,
                        Path(custom_skins_dir) / Path(character) / Path(f"{skin}.png"),
                    )

                    char = open_image(
                        Path(custom_skins_dir) / Path(character) / Path(f"{skin}.png")
                    )

            char = char.resize(
                (
                    int(
                        (char.size[0] * zoom_multipliers[is_singles][size])
                        * portrait_multipliers[size]
                    ),
                    int(
                        (char.size[1] * zoom_multipliers[is_singles][size])
                        * portrait_multipliers[size]
                    ),
                ),
                resample=Image.BOX,
            )

            # TODO: temp
            if size == "L":
                char = char.resize(
                    (
                        int((char.size[0] * 2.0) * portrait_multipliers[size]),
                        int((char.size[1] * 2.0) * portrait_multipliers[size]),
                    ),
                    resample=Image.BOX,
                )
            elif size == "M":
                char = char.resize(
                    (
                        int((char.size[0] * 2.4) * portrait_multipliers[size]),
                        int((char.size[1] * 2.4) * portrait_multipliers[size]),
                    ),
                    resample=Image.BOX,
                )
            elif size == "S":
                char = char.resize(
                    (
                        int((char.size[0] * 2.6) * portrait_multipliers[size]),
                        int((char.size[1] * 2.6) * portrait_multipliers[size]),
                    ),
                    resample=Image.BOX,
                )

        else:
            char = Image.new("RGBA", (0, 0))

        # prevents bad transparency mask errors
        char = char.convert("RGBA")

        # loads layout and replaces default rgb with the chosen new rgb
        layout = replace_rgb(layout, (76, 255, 0), rgb)

        doubles_multipliers = {
            "L": {
                "x": 0.1,
                "y": 0,
            },
            "M": {
                "x": 0.11,
                "y": 0,
            },
            "S": {
                "x": 0.12,
                "y": 0,
            },
        }

        doubles_offsets = {
            "L": {
                "x": 150,
                "y": 0,
            },
            "M": {
                "x": 100,
                "y": 0,
            },
            "S": {
                "x": 30,
                "y": 0,
            },
        }

        doubles_offset_x = 0
        doubles_offset_y = 0

        # handles offsets for the first player in a doubles team
        if is_singles == False and i % 2 == 0:
            doubles_offset_x = char.size[0] * doubles_multipliers[size]["x"]
            doubles_offset_y = 0
        # handles offsets for the second player in a doubles team
        elif is_singles == False and i % 2 == 1:
            doubles_offset_x = -char.size[0] * doubles_multipliers[size]["x"]
            doubles_offset_y = 0

        # pastes character and layout onto the empty portrait
        if character != "None":
            portrait.paste(
                char,
                (
                    int((doubles_offset_x + char_offsets[character][size][0])),
                    int((doubles_offset_y + char_offsets[character][size][1])),
                ),
                char,
            )

        # pastes layout onto characters again to cover overlaps
        portrait.paste(layout, (0, 0), layout)

    # draws nickname rectangle using both top left and bottom right position
    nickname_tl = (4, portrait.size[1] - 60)
    nickname_br = (portrait.size[0] - 5, portrait.size[1] - 4)
    draw_rectangle(portrait, (255, 255, 255), nickname_tl, nickname_br)

    # draws nickname using its bottom right position
    nick_text_br = (portrait.size[0], portrait.size[1] * nickname_multipliers[size])
    draw_text(
        portrait, nickname, (0, 0, 0), 52, nick_text_br, center_text=True, nickname=True
    )

    # draws secondary
    if secondary:
        draw_additional_char(secondary, portrait, (portrait.size[0] - 85, 5))

    # draws tertiary
    if tertiary:
        draw_additional_char(tertiary, portrait, (5, portrait.size[1] - 133))

    # draws placement box
    draw_rectangle(portrait, rgb, (0, 0), (65, 65))

    # draws placement using its bottom right position
    placement_br = (65, 65)
    draw_text(portrait, placement, (255, 255, 255), 64, placement_br, center_text=True)

    # resizes portrait right before quitting
    portrait = portrait.resize(
        (int(portrait.size[0] * resizing), int(portrait.size[1] * resizing)),
        resample=Image.BOX,
    )

    # saves portrait as a separate file
    if save:
        portrait.save(Path(f"./Portraits/{nickname}.png"))

    return portrait


def draw_results(
    top8_image=Image.new("RGBA", (0, 0)),
    title="A Rivals of Aether Bracket",
    attendees_num=0,
    date=datetime.now().strftime("%d-%m-%Y"),
    layout_rgb=(255, 138, 132),
    stage="Aethereal Gates",
    stage_variant=1,
    logo=False,
    logo_offset=[-80, 0],
    save=True,
):
    input_file = Path(f"static/Resources/Backgrounds/{stage}/{stage_variant}.png")

    try:
        bg = Image.open(input_file)
    except FileNotFoundError:
        print(
            "FileNotFoundError: please check your input file and try again.\n"
            rf"Current input file: {input_file}"
        )
        bg = Image.new("RGBA", (0, 0))

    bg = bg.resize((1920, 1080), resample=Image.BOX)

    bg.paste(top8_image, centered_pos(bg, top8_image), top8_image)

    draw_rectangle(bg, layout_rgb, (0, 0), (bg.size[0], 70))
    draw_rectangle(bg, layout_rgb, (0, bg.size[1] - 70), (bg.size[0], bg.size[1]))
    draw_text(bg, f"{title}", (255, 255, 255), 68, (bg.size[0], 70), center_text=True)

    draw_text(
        bg,
        "graphics by @kiirochiicken",
        (255, 255, 255),
        32,
        (10, bg.size[1] - 40),
        anchor="ls",
    )
    draw_text(
        bg,
        "script by @Impasse52",
        (255, 255, 255),
        32,
        (10, bg.size[1] - 10),
        anchor="ls",
    )

    draw_text(
        bg,
        f"{attendees_num} participants",
        (255, 255, 255),
        32,
        (bg.size[0] - 10, bg.size[1] - 40),
        anchor="rs",
    )
    draw_text(
        bg,
        f"{date}",
        (255, 255, 255),
        32,
        (bg.size[0] - 10, bg.size[1] - 10),
        anchor="rs",
    )

    if logo:
        logo_img = Image.open(Path(file_dir) / Path("static/Resources/Layout/logo.png"))
        logo_img = logo_img.resize(
            (int(logo_img.size[0] * 0.25), int(logo_img.size[1] * 0.25))
        )
        bg.paste(logo_img, (bg.size[0] + logo_offset[0], 0 + logo_offset[1]), logo_img)

    if save:
        bg.save("results.png")
