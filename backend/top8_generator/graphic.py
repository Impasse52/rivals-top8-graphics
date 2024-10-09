import logging
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
import json

from PIL import Image
from top8_generator.utils import (
    centered_pos,
    draw_rectangle,
    draw_text,
    open_image,
    paste_image,
    replace_rgb,
)

from .recolor import generate_recolor, start_headless_driver
from .utils import get_latest_file

with open("top8_generator/config/config_de.json") as config:
    config = json.load(config)


char_offsets = config["offsets"]
mode = config["mode"]

file_dir = Path(os.path.dirname(os.path.realpath(__file__)))
char_dir = Path(f"static/Resources/{mode}/Characters/Secondary")
font_dir = Path(f"static/Resources/{mode}/Layout/Pixellari.ttf")

# used to adjust the nicknames' height
nickname_multipliers = config["nickname_multipliers"]

# used to pick the right portrait box
portrait_multipliers = config["portrait_multipliers"]

# different box sizes have different zoom-ins
zoom_multipliers = config["zoom_multipliers"]

# resizes for each playerbox
resizes = config["resizes"]


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
    sizes = ["L", "M", "M", "M", "S", "S", "S", "S"]

    custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent / Path(
        f"static/Resources/{mode}/Characters/Main/Custom"
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
):
    # loads images
    layout = open_image(Path(f"static/Resources/{mode}/Layout/char_portrait.png"))

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
                        f"static/Resources/{mode}/Characters/Main/{character}/{skin}.png"
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
                        (char.size[0] * zoom_multipliers[size])
                        * portrait_multipliers[size]
                    ),
                    int(
                        (char.size[1] * zoom_multipliers[size])
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

        # pastes character and layout onto the empty portrait
        if character != "None":
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
        font_dir,
        52,
        nick_text_br,
        center_text=True,
        nickname=True,
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
    draw_text(
        portrait,
        placement,
        (255, 255, 255),
        font_dir,
        64,
        placement_br,
        center_text=True,
    )

    # resizes portrait right before quitting
    portrait = portrait.resize(
        (int(portrait.size[0] * resizing), int(portrait.size[1] * resizing)),
        resample=Image.BOX,
    )

    # saves portrait as a separate file
    if save:
        portrait.save(Path(f"./Portraits/{nickname}.png"))

    return portrait


def draw_top8_graphic(
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
    logging.info("Starting top 8 generation.")

    bg_dir = Path(f"static/Resources/{mode}/Backgrounds/{stage}/{stage_variant}.png")

    bg = Image.new("RGBA", (0, 0))
    if stage != "Background":
        logging.info(f"Loaded background image from {bg_dir}")
        bg = Image.open(bg_dir)

    bg = bg.resize((1920, 1080), resample=Image.BOX)

    bg.paste(top8_image, centered_pos(bg, top8_image), top8_image)

    draw_rectangle(bg, layout_rgb, (0, 0), (bg.size[0], 70))
    draw_rectangle(bg, layout_rgb, (0, bg.size[1] - 70), (bg.size[0], bg.size[1]))
    draw_text(
        bg,
        f"{title}",
        (255, 255, 255),
        font_dir,
        68,
        (bg.size[0], 70),
        center_text=True,
    )

    draw_text(
        bg,
        "graphics by @kiirochiicken",
        (255, 255, 255),
        font_dir,
        32,
        (10, bg.size[1] - 40),
        anchor="ls",
    )
    draw_text(
        bg,
        "script by @Impasse52",
        (255, 255, 255),
        font_dir,
        32,
        (10, bg.size[1] - 10),
        anchor="ls",
    )

    draw_text(
        bg,
        f"{attendees_num} participants",
        (255, 255, 255),
        font_dir,
        32,
        (bg.size[0] - 10, bg.size[1] - 40),
        anchor="rs",
    )
    draw_text(
        bg,
        f"{date}",
        (255, 255, 255),
        font_dir,
        32,
        (bg.size[0] - 10, bg.size[1] - 10),
        anchor="rs",
    )

    if logo:
        logo_img = Image.open(
            Path(file_dir) / Path(f"static/Resources/{mode}/Layout/logo.png")
        )
        logo_img = logo_img.resize(
            (int(logo_img.size[0] * 0.25), int(logo_img.size[1] * 0.25))
        )
        bg.paste(logo_img, (bg.size[0] + logo_offset[0], 0 + logo_offset[1]), logo_img)

    if save:
        bg.save("results.png")

    logging.info("Succesfully generated graphic.")
