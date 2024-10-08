import React from "react";
import {
    BackgroundsList,
    CharactersList,
    CustomSkinsList,
    PlayerData,
    SkinsList,
    Top8,
    TournamentMeta,
    TournamentSettings,
} from "../types";

// used to retrieve the characters' icons
// TODO: properly implement mode selection
const mode = "roa2";
export const assetsDir = `static/Resources/${mode}/Characters/Secondary`;

// default values for PlayerData
export const defaultPlayerData: PlayerData = {
    nickname: "",
    character: "None",
    skin: "Default",
    custom_skin: false,
    tertiary: "None",
    secondary: "None",
};

// default values for TournamentMeta
export const defaultTournamentData: TournamentMeta = {
    title: "Your Rivals Tournament",
    date: "2022-05-22",
    participants: 0,
    background: "Background",
    background_variant: "1",
    tournament_url: "",
};

// default values for TournamentSettings
export const defaultSettings: TournamentSettings = {
    default_rgb: [76, 255, 0],
    rgb: [55, 72, 128],
    bg_opacity: 100,
    layout: 1,
};

export const defaultSkinList = {
    skin: [""],
};

export const defaultCustoms: CustomSkinsList = {
    character: [{ label: "skin", code: "0000" }],
};

export const defaultBackgrounds = {
    background: 0,
};

export const defaultChars = {
    characters: [],
};

export const skinsListSample = {
    Absa: {
        skin_1: "0000-0000-0000-0000",
        skin_n: "0000-0000-0000-0000",
    },
    Clairen: {
        skin_1: "0000-0000-0000-0000",
        skin_2: "0000-0000-0000-0000",
        skin_n: "0000-0000-0000-0000",
    },
    Elliana: {
        skin_1: "0000-0000-0000-0000",
        skin_2: "0000-0000-0000-0000",
        skin_3: "0000-0000-0000-0000",
        skin_n: "0000-0000-0000-0000",
    },
    Etalus: {},
    Forsburn: {},
    Hodan: {},
    Kragg: {},
    Maypul: {},
    Mollo: {},
    Olympia: {},
    Orcane: {},
    Ori: {},
    Pomme: {},
    Random: "",
    Ranno: {},
    "Shovel Knight": {},
    Sylvanos: {},
    Wrastor: {},
    Zetterburn: {},
};

// retrieves every skin in the backend and sets it as a state variable
export async function getAllSkins(
    setSkinsList: React.Dispatch<React.SetStateAction<SkinsList>>
) {
    const response = await fetch(`/get_all_skins`, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    setSkinsList(await response.json());
}

// retrieves every background in the backend and sets it as a state variable
export async function getAllBackgrounds(
    setBackgroundsList: React.Dispatch<React.SetStateAction<BackgroundsList>>
) {
    const response = await fetch(`/get_all_backgrounds`, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    setBackgroundsList(await response.json());
}

export async function getAllCharacters(
    setCharactersList: React.Dispatch<React.SetStateAction<CharactersList>>
) {
    const response = await fetch(`/get_all_characters`, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    setCharactersList(await response.json());
}

// generates the top8 image and sets the blob URL as a state variable
export async function generateTop8(
    player1: PlayerData,
    player2: PlayerData,
    player3: PlayerData,
    player4: PlayerData,
    player5: PlayerData,
    player6: PlayerData,
    player7: PlayerData,
    player8: PlayerData,
    meta: TournamentMeta,
    settings: TournamentSettings,
    setOutputURL: React.Dispatch<React.SetStateAction<string>>,
    setLoading: React.Dispatch<React.SetStateAction<boolean>>
) {
    const top8: Top8 = {
        1: player1,
        2: player2,
        3: player3,
        4: player4,
        5: player5,
        6: player6,
        7: player7,
        8: player8,
        meta,
        settings,
    };

    setLoading(true);

    var response = await fetch(`/get_top8`, {
        method: "POST",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify(top8),
    });

    // gets new image as a blob and generates an URL for use in the image's link
    var objectURL = URL.createObjectURL(await response.blob());

    setOutputURL(objectURL);

    setLoading(false);

    // saves forms to local storage
    localStorage.setItem("last_top8", JSON.stringify(top8));
}

export async function fetchBracket(
    url: string,
    player1: PlayerData,
    player2: PlayerData,
    player3: PlayerData,
    player4: PlayerData,
    player5: PlayerData,
    player6: PlayerData,
    player7: PlayerData,
    player8: PlayerData,
    meta: TournamentMeta,
    setPlayer1: CallableFunction,
    setPlayer2: CallableFunction,
    setPlayer3: CallableFunction,
    setPlayer4: CallableFunction,
    setPlayer5: CallableFunction,
    setPlayer6: CallableFunction,
    setPlayer7: CallableFunction,
    setPlayer8: CallableFunction,
    setMeta: CallableFunction
) {
    var response = await fetch(`${`/fetch_bracket?url=${url}`}`, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    const response_json = await response.json();

    setPlayer1({ ...player1, nickname: response_json.top8[0] });
    setPlayer2({ ...player1, nickname: response_json.top8[1] });
    setPlayer3({ ...player1, nickname: response_json.top8[2] });
    setPlayer4({ ...player1, nickname: response_json.top8[3] });
    setPlayer5({ ...player1, nickname: response_json.top8[4] });
    setPlayer6({ ...player1, nickname: response_json.top8[5] });
    setPlayer7({ ...player1, nickname: response_json.top8[6] });
    setPlayer8({ ...player1, nickname: response_json.top8[7] });
    setMeta({
        ...meta,
        title: response_json.tournament_name,
        // date: Date.parse(response_json.tournament_date),
        participants: response_json.participants_num,
    });
}
