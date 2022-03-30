async function post_request(address, body) {
    const response = await fetch(`${address}`, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(body),
    });

    return response;
}

async function get_fetch(address) {
    var response = await fetch(`${address}`, {
        method: 'GET',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    return response;
}

// makes an api call to fetch a top 8 from challonge
async function fetch_bracket() {
    const tournament_url_input = document.getElementById("tournament_url");
    if (tournament_url_input.value.length == 0) {
        tournament_url_input.style.backgroundColor = "pink";
    } else {
        // replaces the button's text with a spinner during loading
        // document.getElementById('fetch-button-span').classList.add(["spinner-border"]);
        document.getElementById('fetch-button-span').innerText = "";
        document.getElementById('fetch-button').disabled = true;

        // makes an api call with the specified url to get the bracket's top 8
        const url = document.getElementById('tournament_url').value;
        const response = await get_fetch(`/fetch_bracket?url=${url}`);
        const response_json = await response.json();

        for (var i = 0; i < 8; i++) {
            document.forms[i].children[0].value = response_json["top8"][i];
        }

        document.forms[8].children[0].children[0].value = response_json["tournament_name"];
        document.forms[8].children[0].children[1].value = response_json["participants_num"];
        document.forms[8].children[1].children[0].value = response_json["tournament_date"].substring(0, 10);

        // removes spinner from button and restores text
        document.getElementById('fetch-button-span').classList.remove(["spinner-border"]);
        document.getElementById('fetch-button-span').innerText = "Fetch";
        document.getElementById('fetch-button').disabled = false;
    }
}

// makes an api call to generate the top 8 image and returns it
async function generate_top8_img() {
    const input_is_sane = check_input_sanity();

    if (input_is_sane.every((value) => value == true)) {
        // retrieves top 8 data from forms
        const top8 = get_top8();

        // gets output image element and its link
        var output_img = document.getElementById('output_img');
        var image_link = document.getElementById('img_link');

        // replaces the button's text with a spinner during loading
        document.getElementById('generate-button-span').classList.add(["spinner-border"]);
        document.getElementById('generate-button-span').innerText = "";
        document.getElementById('generate-button').disabled = true;

        // makes an api call to generate the new image
        var response;
        if (arguments[0] == true) {
            // argument check is used to generate image with RoAIT logo (am lazy) 
            response = await post_request('/get_top8?logo=true', top8);
        } else {
            response = await post_request('/get_top8', top8);
        }

        // gets new image as a blob and generates an URL for use in the image's link
        var object_url = URL.createObjectURL(await response.blob());
        image_link.href = object_url;
        output_img.src = object_url;

        // removes spinner from button and restores text
        document.getElementById('generate-button-span').classList.remove(["spinner-border"]);
        document.getElementById('generate-button-span').innerText = "Generate";
        document.getElementById('generate-button').disabled = false;
    }
}

// makes an api call to retrieve every skin for a player's character
async function retrieve_character_skins(player_index) {
    const character = document.forms[player_index - 1].children[1].value;

    const response = await get_fetch(`/get_skins?character=${character}`);
    const response_json = await response.json();
    return response_json.skins;
}

// fills skin list for the selected player
async function fill_skins_select(player_index) {
    // gets player's skin element
    var skin_select = document.forms[player_index - 1].children[2].children[0];

    // re-initializes options to prevent duplicates and non-existent skins
    skin_select.replaceChildren([]);

    // creates skin option element
    skin_option = document.createElement('option');

    // creates default option and appends it
    skin_option.innerText = "Default";
    skin_option.value = "Default";
    skin_select.appendChild(skin_option)

    // retrieves skins from backend and sorts them
    const skins = await retrieve_character_skins(player_index);

    for (var s in skins) {
        skin_option = document.createElement('option');
        skin_option.value = skins[s];
        skin_option.innerText = skins[s];

        skin_select.appendChild(skin_option);
    }

    // adds custom skins from localStorage (after uploading them from a .json)
    const character = document.forms[player_index - 1].children[1].value;
    const skins_json = localStorage.getItem("skins");

    if (skins_json !== null) {
        const custom_skins = JSON.parse(skins_json)[character];

        // create a new option element for each skin and appends it to select
        for (var skin in custom_skins) {
            const custom_skin_option = document.createElement('option');
            custom_skin_option.innerText = skin;
            custom_skin_option.value = custom_skins[skin];

            skin_select.append(custom_skin_option);
        }
    }
}

// makes an api call to retrieve stages
async function get_backgrounds() {
    const background_select = document.getElementById(`background`);

    // if "Empty" is the only option in the select
    if (background_select.options.length == 1) {
        const response = await get_fetch(`/get_backgrounds`);
        const response_json = await response.json();
        const backgrounds = response_json["backgrounds"];
        backgrounds.sort();

        for (const b of backgrounds) {
            background_option = document.createElement('option');
            background_option.value = b;
            background_option.innerText = b;
    
            background_select.options.add(background_option);
        }

    }   
}

// makes an api call to retrieve the selected stage's variants
async function get_bg_variants() {
    const background = document.getElementById(`background`).value;
    const response = await get_fetch(`/get_bg_variants?background=${background}`);
    const response_json = await response.json();
    const variants = response_json.variants;

    document.getElementById(`bg_variant`).replaceChildren(["1"]);

    for (var v in variants) {
        variant_option = document.createElement('option');
        variant_option.value = variants[v];
        variant_option.innerText = variants[v];

        variant_select = document.getElementById(`bg_variant`);

        variant_select.appendChild(variant_option);
    }
}