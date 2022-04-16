import json
import os
import re
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, send_file, send_from_directory
from flask_cors import CORS
from TournamentFetcher import TournamentFetcher

from backend.draw_recolors import generate_top8_recolors
from backend.draw_results import draw_results, draw_top8, draw_top8_columns

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/get_top8", methods=["POST"])
def get_top8():
    logo = bool(request.args.get("logo"))

    top8 = json.loads(list(request.form)[0])

    nicknames = [top8[str(i)]["nickname"] for i in range(1, 9)]
    characters = [top8[str(i)]["character"] for i in range(1, 9)]
    skins = [top8[str(i)]["skin"] for i in range(1, 9)]
    secondaries = [top8[str(i)]["secondary"] for i in range(1, 9)]
    tertiaries = [top8[str(i)]["tertiary"] for i in range(1, 9)]

    if top8["meta"]["date"] != "":
        parsed_date = datetime.strptime(top8["meta"]["date"], "%Y-%m-%d").strftime(
            "%d-%m-%Y"
        )
    else:
        parsed_date = datetime.now().strftime("%d-%m-%Y")

    skin_is_custom = [False for _ in range(0, 8)]

    for i in range(0, 8):
        matched_pattern = re.search("(.{4}-)*(.{4})", skins[i]).group(0)

        if skins[i] == matched_pattern:
            skin_is_custom[i] = True

    if any(skin_is_custom):
        generate_top8_recolors(characters, skins)

    layout = top8["settings"]["layout"]
    if layout == 1:
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
    else:
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

    return send_file(
        "results.png",
        mimetype="image/png",
    )


@app.route("/get_skins")
def get_skins():
    character = request.args.get("character")

    if character != "":
        # module_path = Path(os.path.abspath(rivals_top8_results.__path__[0]))
        resources_path = Path(f"./backend/Resources/Characters/Main/{character}")

        skins = [f.replace(".png", "") for f in os.listdir(resources_path)]
        skins.remove("Default")
        skins.sort()

        return {"skins": skins}

    return {"skins": ["Default"]}


@app.route("/get_backgrounds")
def get_backgrounds():
    # module_path = Path(os.path.abspath(rivals_top8_results.__path__[0])
    resources_path = Path(f"./backend/Resources/Backgrounds")

    return {"backgrounds": os.listdir(resources_path)}


@app.route("/get_bg_variants")
def get_bg_variants():
    background = request.args.get("background")
    # module_path = Path(os.path.abspath(rivals_top8_results.__path__[0])
    resources_path = Path(f"./backend/Resources/Backgrounds/{background}")

    variants = [v.replace(".png", "") for v in os.listdir(resources_path)]

    return {"variants": variants}


@app.route("/fetch_bracket")
def fetch_bracket():
    url = request.args.get("url")

    t = TournamentFetcher(
        challonge_auth={
            "nickname": os.environ["CHALLONGE_NICKNAME"],
            "api_key": os.environ["CHALLONGE_API_KEY"],
        }
    )

    # ! subdomain temporarily hardcoded to true
    tournament = t.tournament(url, subdomain=True)

    participants = (
        tournament.participants[["username", "placement"]]
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
