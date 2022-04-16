function hex_to_rgb(hex_color) {
    const color = hex_color.substring(1, 8);
    const r = Number.parseInt(color.substring(0, 2), 16);
    const g = Number.parseInt(color.substring(2, 4), 16);
    const b = Number.parseInt(color.substring(4, 6), 16);

    return [r, g, b];
}

function rgb_to_hex(rgb) {
    var r = rgb[0].toString(16);
    var g = rgb[1].toString(16);
    var b = rgb[2].toString(16);

    if (r.length == 1)
        r = "0" + r;
    if (g.length == 1)
        g = "0" + g;
    if (b.length == 1)
        b = "0" + b;

    return `#${r}${g}${b}`;
}

/* getters */
function get_settings() {
    const color = document.getElementById("layoutRGB").value.substring(0, 7);
    const rgb = hex_to_rgb(color);

    return {
        "default_rgb": [
            76,
            255,
            0
        ],
        "rgb": [rgb[0], rgb[1], rgb[2]],
        "bg_opacity": 100,
        "layout": Number($('input[name=layout]:checked')[0].id.substring(6, 7)),
        // "bg_opacity": Number(document.getElementById("opacity").value)
    }
}

function get_meta_info() {
    return {
        "title": document.getElementById("title").value,
        "date": document.getElementById("date").value,
        "participants": document.getElementById("participants").value,
        "background": document.getElementById("background").value,
        "background_variant": document.getElementById("bg_variant").value,
        "tournament_url": document.getElementById('tournament_url').value,
    }
}

function get_player_info(current_player) {
    const player_form = document.forms[current_player];

    return {
        "nickname": player_form.children[0].value,
        "character": player_form.children[1].value,
        "skin": player_form.children[2].children[0].value,
        "custom_skin": player_form.children[2].children[1].checked,
        "secondary": player_form.children[3].value,
        "tertiary": player_form.children[4].value,
    };
}

function get_top8() {
    const top8 = {
        "1": get_player_info(0),
        "2": get_player_info(1),
        "3": get_player_info(2),
        "4": get_player_info(3),
        "5": get_player_info(4),
        "6": get_player_info(5),
        "7": get_player_info(6),
        "8": get_player_info(7),
        "meta": get_meta_info(),
        "settings": get_settings(),
    }

    // caches last generated tournament
    localStorage.setItem('lastTop8', JSON.stringify(top8));

    return top8;
}

/* setters */
function set_top8(json) {
    set_player_info(json['1'], 1);
    set_player_info(json['2'], 2);
    set_player_info(json['3'], 3);
    set_player_info(json['4'], 4);
    set_player_info(json['5'], 5);
    set_player_info(json['6'], 6);
    set_player_info(json['7'], 7);
    set_player_info(json['8'], 8);
    set_meta_info(json["meta"]);
    set_settings(json["settings"]);
}

function set_top8_from_local_storage() {
    const top8_json = localStorage.getItem('lastTop8');

    if (top8_json !== null) {
        const top8 = JSON.parse(top8_json);

        // set players, meta and settings if entry exists
        if (top8_json !== null) {
            set_top8(top8);
        }

        // sets custom skins
        for (var i = 1; i <= 8; i++) {
            if (top8[String(i)]["custom_skin"]) {
                custom_skin_checkbox_handler(i);
            }
        }
    }

    // sets uploaded skin .json name
    const upload_button = document.getElementById("upload_skins_label");
    const skin_json_name = localStorage.getItem("skin_json_name");


    if (skin_json_name) {
        upload_button.textContent = `Uploaded JSON: ${localStorage.getItem("skin_json_name")}`;
    }
};

function set_settings(json) {
    const rgb = json["rgb"];
    console.log(rgb_to_hex([rgb[0], rgb[1], rgb[2]]));
    document.getElementById("layoutRGB").value = rgb_to_hex([rgb[0], rgb[1], rgb[2]]); // rgb

    // layout
    const radio_index = json["layout"] - 1;
    $('input[name=layout]')[radio_index].checked = true;
}

function set_meta_info(json) {
    const meta_and_settings_form = document.getElementById('meta-form').children;

    meta_and_settings_form[0].children[0].value = json["title"]; // title
    meta_and_settings_form[0].children[1].value = json["participants"]; // participants
    meta_and_settings_form[1].children[0].value = json["date"]; // date

    meta_and_settings_form[3].children[0].value = json["background"]; // background
    meta_and_settings_form[3].children[1].value = json["background_variant"]; // background variant

    // sets tournament url field
    document.getElementById('tournament_url').value = json["tournament_url"];
}

async function set_player_info(player, index) {
    const player_form = document.forms[index - 1];

    // sets nickname and character
    player_form.children[0].value = player.nickname;
    player_form.children[1].value = player.character;

    // sets skins
    await fill_skins_select(index);
    player_form.children[2].children[0].value = player.skin;

    // sets custom skins
    player_form.children[2].children[1].checked = player.custom_skin;

    // sets secondary and tertiary character
    player_form.children[3].value = player.secondary;
    player_form.children[4].value = player.tertiary;
}


function check_input_sanity() {
    // forms are considered sane by default and are set to non-sane if errors are found
    var sane_forms = [true, true, true, true, true, true, true, true];

    // resets fields marked as non-sane
    for (var i = 0; i < 8; i++)
        document.forms[i].children[2].children[0].style.setProperty("background-color", "white");

    // checks whether the custom skin code is sane for each player form
    for (var i = 0; i < 8; i++) {
        const current_form = document.forms[i];
        const current_char = current_form.children[1].value;
        const skin_field = current_form.children[2].children[0];

        // check custom skin code regex and length if skin field is a text field
        if (skin_field.type == "text") {
            const custom_skin_re = /(.{4}-)*(.{4})/;

            // sanity condition
            sane_forms[i] = custom_skin_re.test(skin_field.value) && skin_field.value.length == code_length[current_char];
        }

        // marks non-sane input fields
        if (!sane_forms[i])
            skin_field.style.setProperty("background-color", "pink")
    }

    // returns array of booleans
    return sane_forms;
}

function upload_handler() {
    var reader = new FileReader();

    // fired when file is uploaded
    reader.onload = (event) => {
        var skins_json = JSON.parse(event.target.result);
        window.localStorage.setItem("skins", JSON.stringify(skins_json));
    };

    // fires onload when it's finished uploading the file
    reader.readAsText(event.target.files[0]);

    const upload_button = document.getElementById("upload_skins_label");
    upload_button.textContent = `Uploaded JSON: ${event.target.files[0].name}`;
    localStorage.setItem("skin_json_name", event.target.files[0].name);
}

function handle_cancel_reset() {
    $('#confirm-reset')[0].style.display = '';
    $('#reset-button')[0].style.backgroundColor = "rgb(28, 31, 35)";
    $('#reset-button')[0].style.color = "white";
    $('#reset-button')[0].innerText = "Reset";
}

function handle_confirm_reset() {
    // reset handler
    set_top8(empty_tournament);

    // resets every custom skin input field
    for (var i = 1; i <= 8; i++) {
        var skin_input = document.forms[i - 1].children[2].children[0];

        // sets text input to select
        if (skin_input.type == "text") {
            var select_skin_input = document.createElement('select');

            // creates default skin option and attaches it to select_skin_input
            var default_skin_option = document.createElement('option');
            default_skin_option.value = "Default";
            default_skin_option.text = "Default";
            select_skin_input.options.add(default_skin_option);

            // adds every class that was applied to the previous input field
            for (var className of skin_input.classList)
                select_skin_input.classList.add(className);

            // sets text field to select
            skin_input.parentElement.replaceChild(select_skin_input, skin_input)
        }

        document.getElementById('confirm-reset').style.display = '';
        document.getElementById('reset-button').style.backgroundColor = 'rgb(28, 31, 35)';
        document.getElementById('reset-button').style.color = 'white';
        document.getElementById('reset-button').innerText = 'Reset';
    };
}

function handle_reset_menu() {
    const settings = $("#confirm-reset")[0];
    const settings_button = $("#reset-button")[0];

    if (settings.style.display == "") {
        // shows menu
        settings.style.display = "block";

        // modifies button
        settings_button.style.backgroundColor = "white";
        settings_button.style.color = "#1c1f23";
        settings_button.innerText = "Are you sure?";
    } else {
        // shows menu
        settings.style.display = "";

        // modifies button
        settings_button.style.color = "white";
        settings_button.style.backgroundColor = "rgb(28, 31, 35)";
        settings_button.innerText = "Reset";
    }
}

function handle_settings_menu() {
    const settings = $(".settings")[0];
    const settings_button = $("#settings-button")[0];

    if (settings.style.display == "") {
        // shows menu
        settings.style.display = "block";

        // modifies button
        settings_button.style.backgroundColor = "white";
        settings_button.style.color = "#1c1f23";
        settings_button.innerText = "Close Settings";
    } else {
        // shows menu
        settings.style.display = "";

        // modifies button
        settings_button.style.color = "white";
        settings_button.style.backgroundColor = "rgb(28, 31, 35)";
        settings_button.innerText = "Settings";
    }
}

function custom_skin_checkbox_handler(player_index) {
    var skin_input = document.forms[player_index - 1].children[2].children[0];


    if (skin_input.type == "select-one") {
        var custom_skin_input = document.createElement('input');
        custom_skin_input.id = `custom_skin_input_${player_index}`;

        // adds every class that was applied to the previous input field
        for (var className of skin_input.classList)
            custom_skin_input.classList.add(className);

        custom_skin_input.placeholder = "Custom Skin"
        custom_skin_input.pattern = "(.{4}-)*(.{4})"

        skin_input.parentElement.replaceChild(custom_skin_input, skin_input)
    } else {
        var select_skin_input = document.createElement('select');

        // creates default skin option and attaches it to select_skin_input
        var default_skin_option = document.createElement('option');
        default_skin_option.value = "Default";
        default_skin_option.text = "Default";
        select_skin_input.options.add(default_skin_option);

        // adds every class that was applied to the previous input field
        for (var className of skin_input.classList)
            select_skin_input.classList.add(className);

        skin_input.parentElement.replaceChild(select_skin_input, skin_input)

        fill_skins_select(player_index);
    }
}

function fill_players_selects(form_id) {
    for (let i = 1; i <= 8; i++) {
        const player_character_select = document.getElementById(`p${i}-${form_id}`);
        characters.forEach((c) => {
            const character_option = document.createElement("option");
            character_option.text = c;
            character_option.value = c;
            player_character_select.options.add(character_option);
        });
    }
}

function handle_doubles_support() {
    for (let i = 0; i < 8; i++)
        document.getElementById(`p${i}-character-doubles`).remove();
}

/* characters list - used to fill selects */
const characters = [
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
    "Random",
    "Ranno",
    "Shovel Knight",
    "Sylvanos",
    "Wrastor",
    "Zetterburn",
];

/* custom skin length for each character */
const code_length = {
    "": 0,
    "Clairen": 54,
    "Forsburn": 54,
    "Zetterburn": 39,
    "Wrastor": 39,
    "Absa": 39,
    "Elliana": 49,
    "Sylvanos": 39,
    "Maypul": 39,
    "Kragg": 34,
    "Orcane": 19,
    "Etalus": 24,
    "Ranno": 39,
    "Ori": 39,
    "Shovel Knight": 34,
    "Mollo": 54,
    "Hodan": 54,
    "Pomme": 49,
    "Olympia": 54,
}

/* empty tournament */
const empty_tournament = {
    "1": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "2": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "3": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "4": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "5": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "6": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "7": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "8": {
        "nickname": "",
        "character": "",
        "skin": "Default",
        "custom_skin": false,
        "secondary": "",
        "tertiary": "",
    },
    "meta": {
        "title": "Your Rivals Tournament",
        "date": "",
        "participants": "0",
        "background": "",
        "background_variant": "1",
        "tournament_url": "",
    },
    "settings": {
        "default_rgb": [76, 255, 0],
        "rgb": hex_to_rgb("#374880"),
        "bg_opacity": 100,
        "layout": 1,
    }
}