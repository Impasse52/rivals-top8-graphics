# useful for offset testing purposes
from PIL.Image import Image
from backend.top8_generator.draw_results import draw_portrait


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


# deprecated layout
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
