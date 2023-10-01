import glob
import os
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import logging

# css path for each character
characters = {
    "Clairen": "#charRow1 > div:nth-child(1)",
    "Forsburn": "#charRow1 > div:nth-child(2)",
    "Zetterburn": "#charRow1 > div:nth-child(3)",
    "Wrastor": "#charRow1 > div:nth-child(4)",
    "Absa": "#charRow1 > div:nth-child(5)",
    "Elliana": "#charRow1 > div:nth-child(6)",
    "Sylvanos": "#charRow2 > div:nth-child(1)",
    "Maypul": "#charRow2 > div:nth-child(2)",
    "Kragg": "#charRow2 > div:nth-child(3)",
    "Orcane": "#charRow2 > div:nth-child(4)",
    "Etalus": "#charRow2 > div:nth-child(5)",
    "Ranno": "#charRow2 > div:nth-child(6)",
    "Ori": "#charRow3 > div:nth-child(1)",
    "Shovel Knight": "#charRow3 > div:nth-child(2)",
    "Mollo": "#charRow3 > div:nth-child(3)",
    "Hodan": "#charRow3 > div:nth-child(4)",
    "Pomme": "#charRow3 > div:nth-child(5)",
    "Olympia": "#charRow3 > div:nth-child(6)",
}

# code length for each character
code_length = {
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


# retrieves the latest saved file on the disk
def get_latest_file(dir):
    list_of_files = glob.glob(f"{dir}/*")
    latest_file = max(list_of_files, key=os.path.getmtime)

    return latest_file


def generate_recolor(driver, character, skin_code):
    """Generate recolor and save it as a new file on the driver-chosen
    downloads directory. Sleep functions are used to ensure that
    HTML elements are loaded before trying to interact with them.
    Using this function in succession and iterating inside this block
    gives extremely similar results, taking ~3.20 seconds to produce
    each custom skin (most of which is spent waiting)."""

    start = time.time()
    logging.info(
        f"Generating recolor for character {character} with skin code {skin_code}"
    )

    char_button = driver.find_element(By.ID, "charSelector")
    char_button.click()

    time.sleep(0.5)

    select_char_button = driver.find_element(By.CSS_SELECTOR, characters[character])
    select_char_button.click()

    time.sleep(0.5)

    # waits for portrait to to avoid char length hiccups
    code_input = driver.find_element(By.ID, "codeInput")

    # make sure that input field is empty, then send skin code
    code_input.clear()
    code_input.send_keys(skin_code)

    time.sleep(1.0)

    # clicks on download button
    download_button = driver.find_element(By.ID, "downImgButton")

    # might be needed to correctly load the download buttons
    time.sleep(0.5)
    download_button.click()

    # clicks on "download portrait" button
    download_portrait_button = driver.find_element(By.CSS_SELECTOR, "#Portait > button")
    download_portrait_button.click()

    time.sleep(1)

    # useful when creating multiple recolors
    back_button = driver.find_element(By.CSS_SELECTOR, "button.okButton:nth-child(3)")
    back_button.click()

    # prevents *.tmp and *.crdownload files from being left around
    time.sleep(0.8)

    logging.info(f"Custom skin portrait generated in {round(time.time() - start, 2)}s.")


def start_headless_driver(download_dir: Path):
    """Starts headless driver with the selected options. Timing is
    kept track of because it is suspected that this module is the
    most time-expensive (parallelization could help)."""

    start = time.time()
    logging.info("Starting headless driver.")

    # set download directory and headless mode
    prefs = {"download.default_directory": str(download_dir)}
    options = Options()
    options.add_argument("--headless=new")
    options.add_experimental_option("prefs", prefs)

    # init and return WebDriver object
    driver = webdriver.Chrome(options=options)

    logging.info(f"Started headless driver in {round(time.time() - start, 2)}s.")

    return driver


if __name__ == "__main__":
    driver = start_headless_driver(
        Path("/home/impasse/Code/Projects/RoA Top 8 Graphics Generator/test")
    )
    driver.get("https://readek.github.io/RoA-Skin-Recolorer/")

    generate_recolor(driver, "Zetterburn", "7E0C-FADC-B97F-FF75-3CF7-0AC4-EB4D-005F")
    generate_recolor(driver, "Ori", "EDE6-FFFC-FAFF-0000-00C3-BFF3-B199-FF09")
    generate_recolor(driver, "Ori", "EADA-EE00-0000-0000-0000-0000-F6F6-F684")
