// calls initialization functions
window.onload = () => {
    fill_players_selects("character");
    fill_players_selects("secondary");
    fill_players_selects("tertiary");
    get_backgrounds();
    set_top8_from_local_storage();

    // settings menu positioning
    const button_bounds = $("#settings-button")[0].getBoundingClientRect();
    $("#settings")[0].style.bottom = button_bounds.height + 490 + "px";
    $("#settings")[0].style.left = button_bounds.x - 0 + "px";
    $("#settings")[0].style.width = button_bounds.width + "px";

    // reset positioning
    const reset_button_bounds = $("#reset-button")[0].getBoundingClientRect();
    $("#confirm-reset")[0].style.bottom = reset_button_bounds.height + 255 + "px";
    $("#confirm-reset")[0].style.left = reset_button_bounds.x + 12 + "px";
    $("#confirm-reset")[0].style.width = reset_button_bounds.width + "px";
};

// handles skins .json upload button
document.getElementById("upload_skins").onchange = upload_handler;

// handles reset buttons
document.getElementById("reset-button").onclick = handle_reset_menu;
document.getElementById("confirm-reset-button").onclick = handle_confirm_reset;
document.getElementById("cancel-reset-button").onclick = handle_cancel_reset;

// handles fetching the bracket from challonge
document.getElementById("fetch-button").onclick = fetch_bracket;

// handles generating the top8 graphic
document.getElementById("generate-button").onclick = generate_top8_img;
document.getElementById("generate-button").oncontextmenu = (e) => { e.preventDefault(); generate_top8_img(true); };

// handles fetching variants for the selected stage
document.getElementById("background").onclick = get_backgrounds;
document.getElementById("background").onchange = get_bg_variants;

// handles settings menu
document.getElementById("settings-button").onclick = handle_settings_menu;

// handles skin-fetching
for (let i = 1; i <= 8; i++) {
    player_character = document.getElementById(`p${i}-character`);
    player_character.onchange = () => fill_skins_select(i);
}

// handles custom skin checkboxes
for (let i = 1; i <= 8; i++) {
    custom_skin_checkbox = document.getElementById(`p${i}-custom-skin-checkbox`);
    custom_skin_checkbox.onchange = () => custom_skin_checkbox_handler(i);
}
