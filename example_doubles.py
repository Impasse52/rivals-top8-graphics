import os
from pathlib import Path
import random
import re

from backend.draw_results import draw_top8
from backend.draw_results import draw_results
from backend.draw_recolors import generate_top8_recolors

if __name__ == "__main__":
    # draw_all_chars("L")

    characters = [
        "Absa",
        "Clairen",
        "Elliana",
        "Etalus",
        "Forsburn",
        "Hodan",
        "Kragg",
        "Maypul",
        "Mollo",
        "Olympia",
        "Orcane",
        "Ori",
        "Pomme",
        "Ranno",
        "Shovel Knight",
        "Sylvanos",
        "Wrastor",
        "Zetterburn",
    ]

    characters = [[random.choice(characters), random.choice(characters)] for _ in range(9)]

    secondaries = ["" for i in range(0, 8)]
    tertiaries = ["" for i in range(0, 8)]

    nicknames = ["" for i in range(0, 8)]

    skins = [
        ["Default", "Default"],
        ["Default", "Default"],
        ["Default", "Default"],
        ["Default", "Default"],
        ["Default", "Default"],
        ["Default", "Default"],
        ["Default", "Default"],
        ["Default", "Default"],
    ]

    custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))) / Path(
        "Resources/Characters/Main/Custom"
    )

    skin_is_custom = [[False, False] for i in range(0, 8)]
    # skin_exists = [[True, True] for i in range(0, 8)]
    for i in range(0, 8):
        for j in range(0, 2):
            matched_pattern = re.search("(.{4}-)*(.{4})", skins[i][j]).group(0)

            if skins[i][j] == matched_pattern:
                skin_is_custom[i][j] = True

    if any(skin_is_custom):
        generate_top8_recolors(characters, skins)

    top8 = draw_top8(
        nicknames,
        characters,
        skins,
        secondaries,
        tertiaries,
        layout_rgb=(255, 138, 132),
        bg_opacity=100,
        resize_factor=1.3,
    )

    draw_results(
        top8,
        title="EU RCS Season 6 Finals",
        attendees_num=89,
        date="24-01-2022",
        stage="Aethereal Gates",
        stage_variant=2,
        layout_rgb=(255, 138, 132),
        logo_offset=(-100, -12),
    )
