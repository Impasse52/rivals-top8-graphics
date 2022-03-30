import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .draw_recolors import generate_recolor, get_latest_file, start_headless_driver

file_dir = Path(os.path.dirname(os.path.realpath(__file__)))
char_dir = Path(file_dir / "Resources/Characters/Secondary")

# used to adjust the nicknames' height
nickname_multipliers = {"L": 1.88, "M": 1.85, "S": 1.83}

# used to pick the right portrait box
portrait_multipliers = {"L": 1, "M": 0.8, "S": 0.75}

# different box sizes have different zoom-ins
zoom_multipliers = {"L": 1.65, "M": 1.75, "S": 1.9}

# xy offsets
char_offsets = {
    "Absa": {
        "L": (-335, -60),
        "M": (-230, -70),
        "S": (-250, -80),
    },
    "Clairen": {
        "L": (-640, -30),
        "M": (-480, -30),
        "S": (-500, -20),
    },
    "Elliana": {
        "L": (-610, -130),
        "M": (-440, -80),
        "S": (-470, -100),
    },
    "Etalus": {
        "L": (-760, 30),
        "M": (-560, 20),
        "S": (-600, 0),
    },
    "Forsburn": {
        "L": (-800, -250),
        "M": (-600, -200),
        "S": (-620, -230),
    },
    "Hodan": {
        "L": (-560, -100),
        "M": (-400, -60),
        "S": (-410, -90),
    },
    "Kragg": {
        "L": (-490, -370),
        "M": (-370, -300),
        "S": (-400, -350),
    },
    "Maypul": {
        "L": (-620, -120),
        "M": (-460, -100),
        "S": (-470, -100),
    },
    "Mollo": {
        "L": (-480, -80),
        "M": (-360, -40),
        "S": (-370, -75),
    },
    "Olympia": {
        "L": (-350, -40),
        "M": (-245, -30),
        "S": (-265, -40),
    },
    "Orcane": {
        "L": (-560, -140),
        "M": (-390, -100),
        "S": (-410, -130),
    },
    "Ori": {
        "L": (-450, -40),
        "M": (-330, -50),
        "S": (-320, -65),
    },
    "Pomme": {
        "L": (-170, -30),
        "M": (-95, -60),
        "S": (-100, -50),
    },
    "Random": {
        "L": (0, 110),
        "M": (30, 80),
        "S": (35, 70),
    },
    "Ranno": {
        "L": (-230, -20),
        "M": (-200, -30),
        "S": (-170, -20),
    },
    "Shovel Knight": {
        "L": (-400, -80),
        "M": (-260, -70),
        "S": (-290, -70),
    },
    "Shovel knight": {
        "L": (-400, -80),
        "M": (-260, -70),
        "S": (-290, -70),
    },
    "Sylvanos": {
        "L": (-690, -120),
        "M": (-500, -80),
        "S": (-530, -100),
    },
    "Wrastor": {
        "L": (-420, 0),
        "M": (-290, -20),
        "S": (-315, -20),
    },
    "Zetterburn": {
        "L": (-660, -250),
        "M": (-500, -220),
        "S": (-510, -230),
    },
    "": {"L": (0, 0), "M": (0, 0), "S": (0, 0)},
}

# old portraits offsets, need to refactor
old_char_offsets = {
    "Absa": {
        "L": (-50, 0),
        "M": (-5, -25),
        "S": (-10, -10),
    },
    "Clairen": {
        "L": (-100, 0),
        "M": (-40, -20),
        "S": (-40, -20),
    },
    "Elliana": {
        "L": (-100, 0),
        "M": (-40, -20),
        "S": (-50, -20),
    },
    "Etalus": {
        "L": (-200, 10),
        "M": (-130, -10),
        "S": (-140, -10),
    },
    "Forsburn": {
        "L": (-160, 0),
        "M": (-80, -20),
        "S": (-80, -15),
    },
    "Hodan": {
        "L": (-490, -70),
        "M": (-230, -60),
        "S": (-270, -70),
    },
    "Kragg": {
        "L": (-140, 0),
        "M": (-90, 0),
        "S": (-70, 0),
    },
    "Maypul": {
        "L": (-120, 120),
        "M": (-30, 60),
        "S": (-60, 30),
    },
    "Mollo": {
        "L": (-320, -40),
        "M": (-230, -40),
        "S": (-250, -30),
    },
    "Olympia": {
        "L": (-210, -30),
        "M": (-140, -30),
        "S": (-150, -30),
    },
    "Orcane": {
        "L": (-160, 0),
        "M": (-80 - 60, -5),
        "S": (-95 + 30, -5 - 20),
    },
    "Ori": {
        "L": (-160, -20),
        "M": (-95, -35),
        "S": (-90, -50),
    },
    "Pomme": {
        "L": (-70, -20),
        "M": (-35, -20),
        "S": (-30, -20),
    },
    "Random": {
        "L": (-130, 0),
        "M": (-90, -20),
        "S": (-90, -40),
    },
    "Ranno": {
        "L": (-110, 10),
        "M": (-60, 10),
        "S": (-80, 0),
    },
    "Shovel Knight": {
        "L": (-100, 0),
        "M": (-35, -5),
        "S": (-40, -5),
    },
    "Shovel knight": {
        "L": (-100, 0),
        "M": (-35, -5),
        "S": (-40, -5),
    },
    "Sylvanos": {
        "L": (-150, 0),
        "M": (-90, -10),
        "S": (-95, -10),
    },
    "Wrastor": {
        "L": (-45, 0),
        "M": (-20, -20),
        "S": (-10, -40),
    },
    "Zetterburn": {
        "L": (-100, 0),
        "M": (-60, 0),
        "S": (-60, -10),
    },
    "": {"L": (0, 0), "M": (0, 0), "S": (0, 0)},
}


# useful for offset testing purposes
def draw_all_chars(size):
    layout_rgb = (0, 230, 200)

    players = [
        draw_portrait("AAAAAAAA", "Absa", "Default", 1, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Clairen", "Default", 2, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Elliana", "Default", 3, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Etalus", "Default", 4, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Forsburn", "Default", 5, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Hodan", "Default", 6, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Kragg", "Default", 7, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Maypul", "Default", 8, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Mollo", "Default", 9, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Olympia", "Default", 10, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Orcane", "Default", 11, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Ori", "Default", 12, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Pomme", "Default", 13, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Random", "Default", 14, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Ranno", "Default", 15, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Shovel Knight", "Default", 16, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Sylvanos", "Default", 17, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Wrastor", "Default", 18, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "Zetterburn", "Default", 19, 2, layout_rgb, size),
        draw_portrait("AAAAAAAA", "", "Default", 20, 2, layout_rgb, size),
    ]

    output = Image.new("RGBA", (players[0].size[0] * 4, players[0].size[1] * 5))

    for i, p in enumerate(players):
        if i == 0:
            output.paste(p, (0, 0), p)
        elif i <= 3:
            output.paste(p, (p.size[0] * i, 0), p)
        elif i > 3 and i <= 7:
            output.paste(p, (p.size[0] * i - p.size[0] * 4, p.size[1]), p)
        elif i > 7 and i <= 11:
            output.paste(p, (p.size[0] * i - p.size[0] * 4 * 2, p.size[1] * 2), p)
        elif i > 11 and i <= 15:
            output.paste(p, (p.size[0] * i - p.size[0] * 4 * 3, p.size[1] * 3), p)
        elif i > 15 and i <= 19:
            output.paste(p, (p.size[0] * i - p.size[0] * 4 * 4, p.size[1] * 4), p)

    output.save("output.png")


def draw_top8_popup():
    layout_rgb = (0, 230, 200)

    players = [
        draw_portrait("AAAAAAAA", "Zetterburn", "Default", 1, 3, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Wrastor", "Default", 2, 1.6, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Sylvanos", "Default", 3, 1.6, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Shovel Knight", "Default", 4, 1.6, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Ranno", "Default", 5, 1.2, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Ori", "Default", 5, 1.2, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Orcane", "Default", 7, 1.2, layout_rgb, "L"),
        draw_portrait("AAAAAAAA", "Maypul", "Default", 7, 1.2, layout_rgb, "L"),
    ]

    output = Image.new(
        "RGBA", (players[0].size[0] + players[1].size[0] * 3, players[0].size[1])
    )

    for i, p in enumerate(players):
        if i == 0:
            output.paste(p, (0, 0), p)
        elif i >= 0 and i <= 3:
            output.paste(
                p, (players[0].size[0] + players[1].size[0] * (i - 1), 0 + 104), p
            )
        elif i > 3:
            output.paste(
                p,
                (
                    players[0].size[0] + players[4].size[0] * (i - 4),
                    players[1].size[1] + 104,
                ),
                p,
            )

    output.save("output.png")


def draw_top8(
    nicknames,
    characters,
    skins,
    secondaries,
    tertiaries,
    resize_factor,
    layout_rgb=(255, 138, 132),
    bg_opacity=100,
    save=True,
):
    # layout settings (from last player to first player)
    placements = [1, 2, 3, 4, 5, 5, 7, 7]
    resizes = [1.223, 0.9, 0.9, 0.9, 0.675, 0.675, 0.675, 0.675]
    sizes = ["L", "M", "M", "M", "S", "S", "S", "S"]

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

    # creates output image
    output = Image.new(
        "RGBA", (players[0].size[0] + players[1].size[0] * 3 - 4, players[0].size[1])
    )

    # pastes portraits onto top8
    # for i, p in enumerate(players):
    #     if i == 0:
    #         pasteImage(p, (0, 0), output)
    #     elif i >= 0 and i <= 3:
    #         pasteImage(p, (players[0].size[0] + players[1].size[0] * (i - 1) - 4, 0), output)
    #     elif i > 3:
    #         pasteImage(p, (players[0].size[0] + players[4].size[0] * (i - 4) - 4, players[1].size[1]), output)

    pasteImage(players[0], (0, 0), output)
    pasteImage(players[1], (players[0].size[0] - 4, 0), output)
    pasteImage(players[2], (players[0].size[0] + players[1].size[0] * 1 - 7, 0), output)
    pasteImage(
        players[3], (players[0].size[0] + players[1].size[0] * 2 - 12, 0), output
    )
    pasteImage(
        players[4],
        (players[0].size[0] + players[4].size[0] * 0 - 4, players[1].size[1]),
        output,
    )
    pasteImage(
        players[5],
        (players[0].size[0] + players[4].size[0] * 1 - 8, players[1].size[1]),
        output,
    )
    pasteImage(
        players[6],
        (players[0].size[0] + players[4].size[0] * 2 - 10, players[1].size[1]),
        output,
    )
    pasteImage(
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
):
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
        pasteImage(players[i], (players[i].size[0] * i + offset_x * i, 0), output)
        pasteImage(
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


def replace_rgb(image, old_rgb, new_rgb, return_image=True):
    img_array = np.array(image)

    r1, g1, b1 = old_rgb
    r2, g2, b2 = new_rgb

    red, green, blue = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    img_array[:, :, :3][mask] = [r2, g2, b2]

    if return_image:
        img_array = Image.fromarray(img_array)

    return img_array


def pasteImage(img, posn, dst):
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
                    # print("the thing is acting dumb again")
                    pass


def centered_pos(pos1, pos2):
    W, H = pos1.size
    w, h = pos2.size

    return (int((W - w) / 2), int((H - h) / 2))


def draw_rectangle(image, rgb, top_left, bot_right):
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle([top_left, bot_right], fill=(rgb))

    return image


def draw_text(image, text, rgb, font_size, bot_right, center_text=False, anchor="lt"):
    font_dir = Path(file_dir / "Resources/Layout/Pixellari.ttf")

    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.truetype(
        font_dir.as_posix(), font_size
    )  # TODO: add a font parameter

    if center_text:
        W, H = bot_right
        w, h = draw.textsize(str(text), font)

        draw.text(((W - w) / 2, (H - h) / 2), str(text), fill=rgb, font=font)
    else:
        draw.text(
            (bot_right[0], bot_right[1]), str(text), fill=rgb, font=font, anchor=anchor
        )

    return image


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
            size[0],
            size[1],
            resample=Image.BOX,
        )

    return image


def draw_additional_char(character, portrait, position):
    input_file = Path(char_dir / f"{character}.png")

    try:
        secondary = Image.open(input_file)
    except FileNotFoundError:
        print(
            "FileNotFoundError: please check your input file and try again.\n"
            rf"Current input file: {input_file}"
        )
        sys.exit(1)

    portrait.paste(secondary, position, secondary)


def draw_portrait(
    nickname,
    character,
    skin,
    placement,
    resizing,
    rgb,
    size,
    secondary=None,
    tertiary=None,
    bg_opacity=100,
    save=False,
):
    # loads images
    layout = open_image(Path(file_dir / "Resources/Layout/char_portrait.png"))

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

    # checks for custom skin
    custom_skin = False

    try:
        matched_pattern = ""
        matched_pattern = re.search("(.{4}-){1}(.{4}-)*(.{4})", skin).group(0)
    except AttributeError:
        pass

    if skin == matched_pattern:
        custom_skin = True

    # returns character image file unless no character is requested
    if character:
        if not custom_skin:
            char_dir = Path(
                file_dir / f"Resources/Characters/Main/{character}/{skin}.png"
            )
            char = open_image(char_dir)
        else:
            # TODO: decouple, create a function that creates every custom skin BEFORE creating the portraits
            # sets some useful directory variables
            custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))) / Path(
                "Resources/Characters/Main/Custom"
            )
            custom_char_dir = (
                Path(custom_skins_dir) / Path(character) / Path(f"{skin}.png")
            )

            # checks if custom skin already exists and uses it, acting as a caching mechanism
            if os.path.exists(custom_char_dir):
                char = open_image(custom_char_dir)
            else:
                # initializes Chrome driver with the desired options
                driver = start_headless_driver(custom_skins_dir)

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
                    (char.size[0] * zoom_multipliers[size]) * portrait_multipliers[size]
                ),
                int(
                    (char.size[1] * zoom_multipliers[size]) * portrait_multipliers[size]
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

    # loads layout and replaces default rgb with the chosen new rgb
    layout = replace_rgb(layout, (76, 255, 0), rgb)

    # prevents bad transparency mask errors
    char = char.convert("RGBA")

    # pastes character and layout onto the empty portrait
    portrait.paste(
        char,
        (
            int((char_offsets[character][size][0])),
            int((char_offsets[character][size][1])),
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
        portrait,
        nickname,
        (0, 0, 0),
        52 if len(nickname) <= 13 else 40,
        nick_text_br,
        center_text=True,
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
    input_file = Path(file_dir / f"Resources/Backgrounds/{stage}/{stage_variant}.png")

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
        "graphics by @Kiirochii",
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
        print(bg.size[0] + logo_offset[0], 0 + logo_offset[1])
        logo_img = Image.open(Path(file_dir) / Path("Resources/Layout/logo.png"))
        logo_img = logo_img.resize(
            (int(logo_img.size[0] * 0.25), int(logo_img.size[1] * 0.25))
        )
        bg.paste(logo_img, (bg.size[0] + logo_offset[0], 0 + logo_offset[1]), logo_img)

    if save:
        bg.save("results.png")
