import os
from pathlib import Path
import re

from draw_results import draw_top8
from draw_results import draw_results
from draw_recolors import generate_top8_recolors

if __name__ == "__main__":
    # draw_all_chars("L")

    characters = [
        "Orcane",
        "Orcane",
        "Orcane",
        "Orcane",
        "Orcane",
        "Orcane",
        "Orcane",
        "Orcane",
    ]

    secondaries = ["" for i in range(0, 8)]
    tertiaries = ["" for i in range(0, 8)]

    nicknames = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]

    skins = [
        "FF00-00FF-FF00-0F0F",
        "Default",
        "Default",
        "Default",
        "Default",
        "Default",
        "Default",
        "Default",
    ]

    custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))) / Path(
        "Resources/Characters/Main/Custom"
    )

    skin_is_custom = [False for i in range(0, 8)]
    # skin_exists = [True for i in range(0, 8)]
    for i in range(0, 8):
        matched_pattern = re.search("(.{4}-)*(.{4})", skins[i]).group(0)

        if skins[i] == matched_pattern:
            skin_is_custom[i] = True

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
