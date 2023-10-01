import json
import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, Response, request, send_file, send_from_directory
from flask_cors import CORS
from TournamentFetcher import TournamentFetcher
import yaml

from top8_generator.draw_results import draw_results, draw_top8, draw_top8_columns

app = Flask(__name__, static_folder="static/build")
CORS(app)


def setup_logging(path: str = "logging.yaml", level=logging.INFO) -> None:
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)
        logging.info(f"Loaded logging config file from {path}.")
    else:
        logging.basicConfig(level=level)
        logging.warning("logging.yaml not found: using basicConfig for logging.")


# setup logging from file
setup_logging(
    path="logging.yaml",
    level=logging.INFO,
)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path) -> Response:
    if path != "" and os.path.exists(f"{app.static_folder}/{path}"):
        return send_from_directory(f"{app.static_folder}", path)

    return send_from_directory(f"{app.static_folder}", "index.html")


@app.route("/get_top8", methods=["POST"])
def get_top8() -> Response:
    logo = bool(request.args.get("logo"))

    # grabs top8 from args and parses it
    top8 = json.loads(list(request.form)[0])

    # for each player, gets nickname, character, skin and additional characters
    nicknames = [top8[str(i)]["nickname"] for i in range(1, 9)]
    characters = [top8[str(i)]["character"] for i in range(1, 9)]
    skins = [top8[str(i)]["skin"] for i in range(1, 9)]
    secondaries = [top8[str(i)]["secondary"] for i in range(1, 9)]
    tertiaries = [top8[str(i)]["tertiary"] for i in range(1, 9)]

    # handles date
    if top8["meta"]["date"] != "":
        parsed_date = datetime.strptime(top8["meta"]["date"], "%Y-%m-%d").strftime(
            "%d-%m-%Y"
        )
    else:
        parsed_date = datetime.now().strftime("%d-%m-%Y")

    # picks the specified layout
    match top8["settings"]["layout"]:
        case 1:
            top8_img = draw_top8(
                nicknames,
                characters,
                skins,
                secondaries,
                tertiaries,
                layout_rgb=tuple(top8["settings"]["rgb"]),
                bg_opacity=top8["settings"]["bg_opacity"],
                resize_factor=1.3,
                save=False,
            )
        case 2:
            top8_img = draw_top8_columns(
                nicknames,
                characters,
                skins,
                secondaries,
                tertiaries,
                layout_rgb=tuple(top8["settings"]["rgb"]),
                bg_opacity=top8["settings"]["bg_opacity"],
                resize_factor=1.3,
                save=False,
            )
        case _:
            raise Exception("No valid layout has been specified.")

    # draws results graphic and saves it to local disk
    draw_results(
        top8_img,
        title=top8["meta"]["title"],
        date=parsed_date,
        attendees_num=top8["meta"]["participants"],
        stage=top8["meta"]["background"],
        stage_variant=top8["meta"]["background_variant"],
        layout_rgb=tuple(top8["settings"]["rgb"]),
        save=True,
        logo=logo,
    )

    # sends the newly generated image to client
    return send_file("results.png")


@app.route("/get_all_skins")
def get_all_skins() -> dict:
    resources_path = Path(f"static/Resources/Characters/Main")

    characters = [f for f in os.listdir(resources_path)]
    skins = {}

    for char in characters:
        skins[char] = [
            f.replace(".png", "") for f in os.listdir(rf"{resources_path}/{char}")
        ]
        skins[char].sort()

    return skins


@app.route("/get_all_backgrounds")
def get_all_backgrounds() -> dict:
    resources_path = Path(f"static/Resources/Backgrounds")

    backgrounds = {}
    for bg in os.listdir(resources_path):
        backgrounds[bg] = len(os.listdir(rf"{resources_path}/{bg}"))

    return backgrounds


@app.route("/get_all_characters")
def get_all_characters() -> dict:
    resources_path = Path(f"static/Resources/Characters/Secondary")

    return {"characters": [f.replace(".png", "") for f in os.listdir(resources_path)]}


@app.route("/fetch_bracket")
def fetch_bracket() -> dict:
    url = request.args.get("url")

    challonge_auth = {
        "nickname": os.environ["CHALLONGE_NICKNAME"],
        "api_key": os.environ["CHALLONGE_API_KEY"],
    }

    t = TournamentFetcher(challonge_auth)

    # ! subdomain temporarily hardcoded to true
    tournament = t.tournament(url, subdomain=True)

    if tournament:
        participants = (
            tournament.participants[["username", "placement"]]  # type: ignore
            .sort_values(by="placement")
            .head(8)["username"]
            .to_list()
        )

        return {
            "top8": participants,
            "participants_num": tournament.participants_count,
            "tournament_name": tournament.tournament_name,
            "tournament_date": tournament.started_at,
        }

    return {}


# deprecated
@app.route("/get_skins")
def get_skins() -> dict:
    character = request.args.get("character")

    if character != "":
        # module_path = Path(os.path.abspath(rivals_top8_results.__path__[0]))
        resources_path = Path(f"./Resources/Characters/Main/{character}")

        skins = [f.replace(".png", "") for f in os.listdir(resources_path)]
        skins.remove("Default")
        skins.sort()

        return {"skins": skins}

    return {"skins": ["Default"]}


@app.route("/get_backgrounds")
def get_backgrounds() -> dict:
    # module_path = Path(os.path.abspath(rivals_top8_results.__path__[0])
    resources_path = Path(f"static/Resources/Backgrounds")

    return {"backgrounds": os.listdir(resources_path)}


@app.route("/get_bg_variants")
def get_bg_variants() -> dict:
    background = request.args.get("background")
    # module_path = Path(os.path.abspath(rivals_top8_results.__path__[0])
    resources_path = Path(f"./Resources/Backgrounds/{background}")

    variants = [v.replace(".png", "") for v in os.listdir(resources_path)]

    return {"variants": variants}
