import glob
import os
from pathlib import Path
import re
import time
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

recolors = {
    0: {
        "Character": "Orcane",
        "Code": "994C-E2FF-DE00-7F00",
    },
    1: {
        "Character": "Pomme",
        "Code": "A17D-5DD7-0000-BC5B-E500-0000-FFCC-00FF-0000-9600",
    },
    2: {
        "Character": "Pomme",
        "Code": "E8D9-D300-1C5F-0049-9600-9FCA-FFB3-22D2-7BFF-A400",
    },
    3: {
        "Character": "Kragg",
        "Code": "551C-7AFF-FFFF-9D47-D4E5-6600-6700",
    },
    4: {
        "Character": "Olympia",
        "Code": "42FE-842B-FF4B-4538-42C4-237B-FFFF-FFFF-FFFF-00FF-5377",
    },
    5: {
        "Character": "Olympia",
        "Code": "F5A9-B8F5-A9B8-F2DB-C2F5-A9B8-5BCE-FAFF-F9F9-5BCE-FA8A",
    },
    6: {
        "Character": "Elliana",
        "Code": "1111-5DD7-0000-BC5B-E500-0000-FFCC-00FF-1111-9600",
    },
    7: {
        "Character": "Mollo",
        "Code": "FF00-00A6-0000-3112-1231-1212-FF00-00FF-0000-000D-202F",
    },
}


def get_latest_file(dir):
    list_of_files = glob.glob(f"{dir}/*")
    print(list_of_files)
    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file


def generate_recolor(driver, character, skin_code):
    char_button = driver.find_element(By.ID, "charSelector")
    char_button.click()

    select_char_button = driver.find_element(By.CSS_SELECTOR, characters[character])
    select_char_button.click()

    # waits for portrait to to avoid char length hiccups
    time.sleep(0.2)

    code_input = driver.find_element(By.ID, "codeInput")

    if len(skin_code) == code_length[character]:
        code_input.send_keys(skin_code)

    # clicks on download button
    download_button = driver.find_element(By.ID, "downImgButton")

    # might be needed to correctly load the download buttons
    # time.sleep(0.1)
    download_button.click()

    # clicks on "download portrait" button
    download_portrait_button = driver.find_element(By.ID, "Portrait")
    download_portrait_button.click()

    # useful when creating multiple recolors
    back_button = driver.find_element(By.CSS_SELECTOR, "button.okButton:nth-child(3)")
    back_button.click()

    # prevents *.tmp and *.crdownload files from being left around
    time.sleep(0.5)


def generate_recolors_sequence(driver, skins_dict, dir):
    # a temporary folder is needed to prevent same-name conflicts, useful for proper renames
    try:
        os.mkdir("tmp")
    except FileExistsError:
        pass

    for entry in skins_dict:
        generate_recolor(
            driver, skins_dict[entry]["Character"], skins_dict[entry]["Code"]
        )
        filename = get_latest_file(dir)

        try:
            os.rename(filename, f"{skins_dict[entry]['Code']}.png")
        except FileExistsError:
            pass

        try:
            shutil.move(f"{skins_dict[entry]['Code']}.png", "./tmp")
        except shutil.Error:
            pass

    # moves files to requested dir
    for file in os.listdir("./tmp"):
        if file not in os.listdir(dir):
            shutil.move(file, dir)

    # deletes temp folder
    shutil.rmtree("./tmp")


def start_headless_driver(download_dir=os.path.dirname(os.path.realpath(__file__))):
    prefs = {"download.default_directory": str(download_dir)}

    # sets options
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def create_named_recolors(driver, character, recolors_dict):
    try:
        os.mkdir(character)
    except FileExistsError:
        pass

    custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))) / Path(
        character
    )

    # gets recolorer webpage
    driver.get("https://readek.github.io/RoA-Skin-Recolorer/")

    for entry in recolors_dict:
        generate_recolor(driver, character, recolors_dict[entry])
        filename = get_latest_file(custom_skins_dir)
        os.rename(
            Path(custom_skins_dir) / Path(filename),
            Path(custom_skins_dir) / Path(f"{entry}.png"),
        )


def generate_top8_recolors(characters, skins):
    # sets some useful directory variables
    custom_skins_dir = Path(os.path.dirname(os.path.realpath(__file__))) / Path(
        "Resources/Characters/Main/Custom"
    )

    # initializes Chrome driver with the desired options
    driver = start_headless_driver(custom_skins_dir)

    # gets recolorer webpage
    driver.get("https://readek.github.io/RoA-Skin-Recolorer/")

    for i in range(0, 8):
        character = characters[i]
        skin = skins[i]

        matched_pattern = re.search("(.{4}-)*(.{4})", skin).group(0)

        # not a custom skin - skipping
        if skin != matched_pattern:
            continue

        custom_char_dir = Path(custom_skins_dir) / Path(character) / Path(f"{skin}.png")

        # custom skin already exists - skipping
        if os.path.exists(custom_char_dir):
            pass
        else:
            # create recolor of the requested character and skin code
            generate_recolor(driver, character.title(), skin)

            # gets latest created file and renames it
            filename = get_latest_file(custom_skins_dir)

            # tries to create custom skins folder for the specified character
            try:
                os.mkdir(Path(custom_skins_dir) / Path(character))
            except FileExistsError:
                pass

            shutil.move(
                filename,
                Path(custom_skins_dir) / Path(character) / Path(f"{skin}.png"),
            )

    driver.close()


absa = {
    "Default": "7879-A1E7-79B9-82AD-B1BB-9B8F-D6D7-F4EE",
    "Blue": "687F-B269-DEFF-90AB-C0BB-9B8F-C6DD-FF36",
    "Red": "AE70-69FF-7272-B979-A2BB-9B8F-FFD2-CCE6",
    "Green": "ACB2-694F-FF4F-72C0-87BB-9B8F-FFFF-C8F5",
    "Grey": "4F4F-4FFA-FAFA-9999-99BB-9B8F-B3B3-B3C3",
    "Purple": "743F-84FB-FF79-FBFF-79BB-9B8F-D290-E86E",
    "Christmas": "F3D9-D56D-C253-DE48-48DE-4848-FFFF-FFA0",
    "Valentines": "FFA6-D4D1-3030-DE49-77FF-F6D1-FFFF-FFB4",
    "Summer": "F6EC-7259-CCE9-9BF9-D1FF-B957-FFFD-D36D",
    "Halloween": "444D-6BFA-7AFF-FF7C-0044-4D6B-B1FF-6B3D",
    "Default Custom 1": "CCCC-CCF9-FF62-988C-B7FF-EBBA-FBFD-FFD7",
    "Default Custom 2": "6716-164B-4B4B-A42F-FF53-3A3A-D696-7116",
    "Twitch": "6441-A5ED-DEFF-937E-B8FF-DFC3-FFFF-FF71",
    "Champion": "3F3F-46B2-FFD0-F5FE-FFFF-FFFF-C6C6-D411",
    "Abyss": "745E-8776-73B9-DC71-FFDC-71FF-A6AC-D60C",
    "Early Access": "A7BA-4A53-7A3E-D3E2-9AD3-E29A-D3E2-9AA7",
    "Penguin": "3F3F-3F4D-83FF-E742-FFFF-DD55-FFFF-FFD2",
    "Golden": "FFDD-1EFF-F2BA-FCD5-35E3-A40A-FFF7-CAD7",
    "Ranked": "FFCC-0083-83B0-FFFF-FFFF-8700-E4E4-F045",
    "Steampunk": "30DA-A5A2-5D34-0FFF-EB59-423D-D3F8-ECA5",
}

clairen = {
    "Default": "4136-5045-4559-AA22-4AB5-B5B5-FFE6-63FF-0D6A-00FF-F7B9",
    "Blue": "4136-5045-4559-4076-FFB5-B5B5-FFE6-6346-00C6-00ED-FCC0",
    "Orange": "4136-5045-4559-FF64-40B5-B5B5-FFE6-63DC-8700-FF00-0040",
    "Green": "4136-5045-4559-40FF-40B5-B5B5-FFE6-6300-DC5E-FCFF-00C9",
    "Purple": "5425-5D83-6D9B-483D-4BC5-C0D2-FFAF-51B0-3FFF-FFA8-1FEA",
    "White": "96A3-A46D-8D9B-FFFF-FFEF-E9FF-FF2F-2F00-CBC4-FF35-3501",
    "Christmas": "F6E8-E825-2525-0CAA-00FF-4848-FFFF-FFE1-0000-00FF-1E99",
    "Valentines": "E4E4-E477-3E3E-FF9A-E4A7-7C99-FF7D-A8EF-71BB-E34B-4BE9",
    "Summer": "FFA6-2859-CCE9-FFF6-8CFF-FDE5-FFA6-28FF-D820-59CC-E90E",
    "Halloween": "A3E7-9E7E-7E7D-9683-5BAA-A598-6156-45A7-3E86-FF77-00C8",
    "Default Custom 1": "3E54-3B37-4F34-8998-7A38-6B45-9A77-1A2A-A857-FFBE-00F7",
    "Default Custom 2": "3A3A-4672-7F92-53E0-FB35-61AC-203D-6914-0E10-FFFF-E442",
    "Genesis": "3435-3756-5656-FAF7-F7B5-B5B5-FF39-3FFF-CEE1-FE2F-3536",
    "Hero": "4136-50FE-FED8-6096-61A0-7857-8B61-4943-A4D6-FAD4-3EAC",
    "Abyss": "4F3D-5E56-5492-DC71-FFA6-ACD6-903B-CEA6-ACD6-DC71-FFF9",
    "Early Access": "A9BA-4A23-4331-537A-3ED3-E29A-D3E2-9AA7-BA4A-2343-314A",
    "Arcade (Green)": "FFFF-FF41-3F36-8CDE-5E41-3F36-C6CB-2FD4-D4D4-7AEC-3AA7",
    "Arcade (Pink": "FFFF-FF41-3F36-D987-CD41-3F36-C6CB-2FD4-D4D4-FE6A-E83B",
    "Arcade (Blue)": "FFFF-FF41-3F36-91D2-F341-3F36-C6CB-2FD4-D4D4-6DCE-FFB1",
    "Infamous": "5653-AA33-3741-37EA-FFF6-FFFF-D445-FED4-45FE-00FF-A8B9",
    "Champion": "413E-3752-5252-B2FF-D0D0-DFDE-B2FF-D0D0-DFDE-7FFF-B168",
    "Ranked": "FFCC-00FF-8700-E4E4-F079-7AC3-F3FC-FFBE-5723-FFD8-3D9D",
    "Golden": "FCFC-FC75-5C00-FFDD-1EFC-D535-FFDD-1EA9-A9A9-FFDD-1E5B",
    "Heat Wave": "302F-238F-1212-1E0A-A3A4-6D39-CDB8-39C5-0000-FFD7-5A78",
}

elliana = {
    "Default": "D580-5796-9C91-AF91-C89D-D454-89C6-C248-453C-9100",
    "Blue": "6194-D7C9-CDC8-9399-CA67-D5AF-7A8F-A548-453C-8F00",
    "Red": "CD5E-54C9-CDC8-C491-91E7-B256-A590-7A48-453C-E700",
    "Green": "6AD5-72E4-C259-C7C0-8F8E-D547-A0A5-7A48-453C-AE00",
    "Grey": "5050-50E4-EEFF-C7BF-BF93-93BA-AAAA-AA48-453C-FC00",
    "Pink": "A956-90DA-BAD0-FFFE-FFFF-FFFF-AAAA-AA86-3F95-1100",
    "Christmas": "FF22-22FF-FFFF-B582-523E-BC3B-3E3E-3ECC-2222-A900",
    "Valentines": "FF99-D2FF-FFFF-FFD9-EDE3-4B4B-A077-8EB7-0070-1F00",
    "Summer": "59CC-E9FF-F68C-FFD8-A1FF-A628-AC51-004E-453C-C100",
    "Halloween": "FF94-2230-3430-9BAB-6C52-AD54-6743-15CC-8516-1600",
    "Default Custom 1": "0052-BCFF-FFFF-FFFF-FFFF-FFFF-FFFF-FF8B-7EC7-9600",
    "Default Custom 2": "3C1F-1FA5-2623-FAFB-59FC-8506-ECD5-16E0-500F-EB00",
    "Arcade (Green)": "413F-368C-DE5E-FFFF-FFFF-FFFF-FFFF-FF41-3F36-1900",
    "Arcade (Pink)": "413F-36D9-87CD-FFFF-FFFF-FFFF-FFFF-FF41-3F36-DE00",
    "Arcade (Blue)": "413F-3691-D2F3-FFFF-FFFF-FFFF-FFFF-FF41-3F36-CB00",
    "Abyss": "4F3D-5EA6-ACD6-DC71-FF92-3BCE-4E17-8D4E-178D-3D00",
    "Early Access": "537A-3ED3-E29A-D3E2-9AA7-BA4A-537A-3E53-7A3E-7F00",
    "Infamous": "5653-AAD4-45FE-37EA-FF00-FFA8-FFFF-FF33-3741-0900",
    "On The Edge": "3A3A-3AFF-C531-FFFF-61FF-7C00-D0CB-AF3A-3A3A-C400",
    "Champion": "3F3F-46D0-DFDE-D0DF-DEB2-FFD0-B2FF-D052-5252-9F00",
    "Ranked": "FFCC-00E4-E4F0-FFD8-3DE4-E4F0-BE57-23E0-500F-F200",
    "Golden": "FFDD-1EFF-FCD6-FCFA-F89F-7217-B389-0FFF-DD1E-3C00",
}

etalus = {
    "Cyan": "73B9-BAA6-B7FE-F5FF-FFA2",
    "Yellow": "F9FF-B2FF-9BAB-5F27-2015",
    "Green": "4F71-56A6-F7B4-CCCD-400C",
    "Brown": "554D-4CEE-D0B6-AF89-6B33",
    "Pink": "FCFA-FCFF-9EEE-4B35-529F",
    "Christmas": "FDEB-E86D-C253-DE48-4819",
    "Valentines": "FFEC-F7E3-4B4B-E661-A95E",
    "Summer": "59CC-E9FF-F68C-FFA6-2809",
    "Halloween": "3EB6-5A9F-ADB1-3635-350C",
    "Default Custom 1": "2930-3464-8B8C-7E39-3919",
    "Default Custom 2": "8355-84EF-EFEF-5947-5DF0",
    "Champion": "D0DF-DE5A-5A5A-FFFF-FFA6",
    "Golden": "FDFB-F4FF-DC1E-4344-5791",
    "Abyss": "A6AC-D674-5E87-5654-929E",
    "Early Access": "D3E2-9A53-7A3E-2343-31FF",
    "Panda": "FBFA-FC7F-EF67-4344-57E6",
    "Genesis": "4644-44E0-0B00-F6EF-EFD8",
    "Ranked": "FFCC-00E4-E4F0-FF87-0068",
}

forsburn = {
    "Blue": "3270-9180-601C-A9FF-DA3F-B1EB-0030-770F-3143-FFFF-E400",
    "Red": "9132-4480-601C-FFBA-87FF-5F5F-A001-2A43-0F19-FFFF-E44E",
    "Green": "6591-3280-601C-D2FF-001F-DD00-007F-0F2B-430F-FFFF-E44B",
    "White": "B3B3-B380-601C-D5D6-D983-8588-4040-414B-4B4B-FFFF-E4E2",
    "Purple": "7732-9180-601C-C281-FF6D-36C1-4A00-AA35-1342-FFFF-E4FB",
    "Christmas": "DE48-6C6D-C253-FFFF-FFF6-BEC4-FDEB-E872-0000-FFFC-FC2C",
    "Valentines": "B700-70A0-778E-FFAC-FEF7-4CD5-D700-8E6A-002D-FFFF-FF16",
    "Summer": "FFA6-2859-CCE9-FFF6-8CD0-C649-FFA6-2875-4A0F-FFFF-E4EA",
    "Halloween": "4B19-65CB-CDB6-FF7C-00A7-3E85-7729-5D13-061A-FBFC-F1A4",
    "Default Custom 1": "2D2D-2D46-1933-FFFF-3CF7-C00A-EB88-0000-0000-FFFF-E46E",
    "Default Custom 2": "3A3A-4672-7F92-53E0-FB35-61AC-203D-6914-0E10-FFFF-E442",
    "Genesis": "FAF7-F73E-3F3F-FF39-3FFF-393F-FF39-3FC1-B1B1-FAF7-F7AD",
    "Heatwave": "0400-A330-2F23-FFEF-3BCF-5E17-A400-00BF-8700-FFFF-FFFD",
    "Abyss": "4F3D-5E56-5492-DC71-FF92-3BCE-4E17-8D15-0F1B-E4F6-FFF2",
    "Early Access": "537A-3EA7-BA4A-D3E2-9AA7-BA4A-2343-3123-4331-D3E2-9A3C",
    "Champion": "B2FF-D041-3E37-FFFF-FFD0-DFDE-D0DF-DE67-9378-FFFF-E4C3",
    "Ranked": "FFCC-0030-2F23-FFCC-00E4-E4F0-0000-00FF-8700-E4E4-F0D0",
    "Golden": "FFDD-1EE1-BA25-FFFF-FFFD-FFFC-FFF8-C48E-5C00-FFF7-CAFC",
}

hodan = {
    "Blue": "4194-D4BE-E0FF-0C3C-5EB8-DFE1-E685-196C-C7D0-165B-8F71",
    "Red": "DC5B-5BC8-C8C8-3C3C-3CC8-C8C8-A102-13D4-3434-A400-0019",
    "Green": "91E3-5B2F-8765-5C6F-56DC-71FF-FCFC-FC91-E35B-6EAC-454A",
    "Grey": "B4B4-B4E4-C8C8-8B4F-2883-8588-CDCE-D14D-4D4D-2E2E-2EBB",
    "Purple": "E0AE-EB96-A3A4-6F5E-A677-3291-FF35-35F7-E6F6-C8B2-D02D",
    "Christmas": "D4EE-F37C-CEFF-7CCE-FFFF-2D34-FFE4-32FF-FFFF-FEFF-FFD4",
    "Valentines": "FFA9-F8E6-49AF-FF6F-96EF-2D34-FFFF-FFFF-DEED-FCB4-E84A",
    "Summer": "17CD-FFFF-FFE4-EF61-432D-BDEF-4E3C-FFFF-C14B-D182-3D78",
    "Halloween": "7DE2-690C-4B65-4FBD-139E-BFD1-EEEE-EE53-8D62-4363-4B03",
    "Default Custom 1": "DEB5-00FF-D096-FFD0-96F3-2F1F-E2AA-2E76-5441-6E3B-2094",
    "Default Custom 2": "FFC5-2643-BD47-43BD-47CF-9C00-FFCE-CEFF-8C0D-E139-01FF",
    "Abyss": "A6AC-D6A6-ACD6-5654-92DC-71FF-913B-CE4F-3D5E-3827-46DB",
    "Early Access": "D3E2-9AA7-BA4A-537A-3E23-4331-A7BA-4AD3-E29A-D3E2-9A69",
    "Ranked": "EBDE-7BE9-E9E8-FF9E-27CD-70DE-7E00-7EFF-F88F-F8D1-6174",
}

kragg = {
    "Blue": "526A-A86E-C4C5-DBD5-DD1C-3B4D-A500",
    "Pink": "AA49-68CA-8E61-FFE1-684F-183D-E100",
    "Green": "4181-42A5-7575-D7DD-D51A-2D12-1100",
    "Grey": "6379-8159-5959-DCDA-D61E-2E2D-2300",
    "Purple": "675D-88AD-6483-D9E7-D51D-1F34-5600",
    "Christmas": "FFEB-EBE1-4141-6DC2-5373-0000-6D00",
    "Valentines": "FF82-CBFF-C1FF-FFEC-F7BA-2A24-6700",
    "Summer": "D0C6-4959-CCE9-9BF9-D45C-571F-E300",
    "Halloween": "B16D-2361-5645-A3E7-9E3C-2424-E700",
    "Default Custom 1": "DE6C-2561-3131-B466-3B46-1B00-5800",
    "Default Custom 2": "FFFF-FF61-83A5-BDAA-D52C-1B4E-E800",
    "Summit (White)": "D1D5-DD4B-5068-BCC2-CE1E-2432-2A00",
    "Summit (Red)": "AC08-274B-5068-BCC2-CE1E-2432-A900",
    "Champion": "82AD-B141-3E37-5E56-4D39-3F4B-0300",
    "Abyss": "4F3D-5E56-5492-DC71-FF15-0F1B-8B00",
    "Early Access": "537A-3EA7-BA4A-D3E2-9A23-4331-9900",
    "Burrito": "AA95-3ADB-4C53-A9F5-7C32-333E-9E00",
    "Golden": "FFBB-00FF-FFFF-FFFD-FB6B-4E1C-4A00",
    "Ranked": "FFCC-005C-6160-C4FF-F662-4C00-E800",
    "Genesis": "302B-2DF8-5C69-D6DF-EA16-1415-2B00",
}

maypul = {
    "Blue": "4E7C-9CC3-FBFC-7FFD-FF41-3E37-C387-652D",
    "Red": "9A45-45FF-CFF1-FF80-8341-3E37-C387-65D6",
    "Yellow": "9A86-45FF-FFDF-FDF6-8141-3E37-C387-650C",
    "Grey": "666A-6DFF-E6E1-FAFA-FA41-3E37-C387-6545",
    "Purple": "7A6F-9BBE-EBF7-7F90-FF41-3E37-C387-6536",
    "Christmas": "DE48-48FF-B5A7-44B3-22FC-FFFF-FCFF-FF9D",
    "Valentines": "FF85-D8FF-FFFF-D850-5091-2222-FFEC-F7FE",
    "Summer": "59CC-E9FF-F68C-FFA6-2859-CCE9-FFF6-8C93",
    "Halloween": "FFF8-E2B3-AB7C-CCC2-8EB3-AB7C-FFF8-E2EA",
    "Default Custom 1": "FFA4-CDFF-FFA6-D781-4141-3E37-C087-651C",
    "Default Custom 2": "FFFF-FF93-A8F7-004C-3B59-4883-5C40-27DA",
    "Panda": "FFFF-FFFF-FFFF-FF9A-B41E-1E1E-9995-7CC7",
    "Arcade (Blue)": "413E-3791-D2F3-D3ED-FB41-3E37-91D2-F330",
    "Arcade (Green)": "413E-378C-DE5E-E4F2-7C41-3E37-8CDE-5EEA",
    "Arcade (Pink)": "413E-37D9-87CD-F1C3-F341-3E37-D987-CD95",
    "Abyss": "5654-92A6-ACD6-DC71-FF4F-3D5E-4F3D-5E6B",
    "Early Access": "5378-3ED3-E29A-A7BA-4A53-7A40-D3E2-9AEB",
    "Golden": "FFDC-1EFF-FFFF-FFDC-1EFF-DC1E-FFE6-1E04",
    "Champion": "5252-52D0-DFDE-B2FF-D03F-3F46-C9C9-DC5D",
    "Ranked": "FFCC-00E4-E4F0-E4E4-F000-0117-FFBA-279A",
}

mollo = {
    "Blue": "4756-6337-383B-11B0-CB43-5E79-00E2-FFA8-E4FF-0000-0099",
    "Red": "AD37-37DF-DFDF-B591-8951-4646-FF7C-7CFF-B387-3D07-0789",
    "Green": "5143-3CFF-F5E0-EAB4-4F3A-6B46-4CB7-4035-CE35-001E-05F7",
    "White": "FFFF-FF35-393A-A9B1-BC7C-8485-E7FA-FFAF-C5CE-1E1E-1E89",
    "Pink": "FEFF-FFFF-9EE5-43AE-D83C-3C3C-F74D-C77F-DAFF-2E0D-25CB",
    "Christmas": "8149-3AE7-4949-45CD-42E1-ECEE-FF49-3188-E041-0320-0810",
    "Valentines": "FFEE-F7FF-DAED-B626-2759-3E50-FF7F-FFFF-4747-2900-2E79",
    "Summer": "F29A-30FF-F9A1-D63D-3D1A-5A72-28D4-FF3D-EFFF-2C18-0F53",
    "Halloween": "6360-5984-7970-A8A1-9E41-3D3B-E7CA-ADFF-CBCB-FF00-00E8",
    "Default Custom 1": "8251-31ED-D8B6-C493-684C-2E1B-FFFB-E9FF-9136-1608-0202",
    "Default Custom 2": "5E67-72D2-F2E6-8EFF-D701-395E-3DD8-FFED-EDED-0014-21CA",
    "Abyss": "5654-9285-6E96-A6AC-D64F-3D5E-DC71-FFE2-A0E1-1610-1CA6",
    "Early Access": "537A-3ED3-E29A-A7BA-4A23-4331-A7BA-4AD3-E29A-2343-31F4",
    "Ranked": "A260-A0D2-D2D2-FDD2-5152-2B5A-FFE9-00FF-6E00-0000-0030",
}

olympia = {
    "Blue": "C6CE-E3EE-F8FE-E2CD-B3DD-9494-1E6B-91FF-F9F9-0032-BCC8",
    "Red": "F5C6-00FF-E681-C19E-6ADD-9494-DC19-19FF-F9F9-2252-D91F",
    "Green": "85C5-4728-9933-9156-468F-6E59-2A3B-30FF-FBE9-719B-6F31",
    "White": "7E7F-80D9-DADB-BDBC-BDBA-ADA2-4D48-48FF-F9F9-701C-82A9",
    "Dark Purple": "E412-66ED-0080-6B40-5D51-5052-4741-4FFF-F9F9-F5ED-4CF8",
    "Christmas": "5BB7-3AFE-FFFE-A17B-72E4-8574-CA20-2CFF-FFFF-2672-4E47",
    "Valentines": "CF22-2DFF-D5FE-7048-48F1-D8E7-FF58-CBFF-F9F9-3296-4F33",
    "Summer": "8DEC-AFDB-FFF9-EDC2-75E4-8574-8DEB-F6CA-F3FF-3296-7BBD",
    "Halloween": "C88D-ECC6-B8EC-8E6D-5C6E-9986-A1CE-62FF-FFFF-FF00-0088",
    "Default Custom 1": "17A6-7317-A673-99D7-F255-8568-F5DB-8BFF-F9F9-16D9-9431",
    "Default Custom 2": "C517-38C5-1738-E4DA-BAE4-8574-D6CF-F5FF-F9F9-32DB-9675",
    "Abyss": "C81F-FFF0-A9FF-5654-924F-3D5E-A6AC-D6DA-B9FF-4F3D-5DFC",
    "Early Access": "D3E2-9AD3-E29A-537A-3EA7-BA4A-D3E2-9AD3-E29A-2343-3105",
    "Ranked": "FFD2-2FFF-D22F-FFFE-F9E1-9E00-C489-CDFF-F9F9-2343-31C4",
}

orcane = {
    "Cyan": "1BAA-A8FA-FFFF-C800",
    "Red": "CE30-30FF-DAA1-6E00",
    "Green": "237A-35F8-FF86-9700",
    "Grey": "393A-3CFF-FFFF-8800",
    "Purple": "6937-73FF-EF37-B700",
    "Christmas": "DE48-486D-C253-7200",
    "Valentines": "FF84-C1FF-ECF7-C000",
    "Summer": "59CC-E9FF-F68C-9800",
    "Halloween": "CAFF-EACA-FFEA-7F00",
    "Default Custom 1": "FFFF-FF2E-2E2E-5400",
    "Default Custom 2": "EC6C-77F0-C3BF-B200",
    "Golden": "ECC9-21EC-C921-C800",
    "Summit": "3A3B-53DA-193C-1400",
    "Abyss": "4F3D-5EA6-ACD6-9300",
    "Early Access": "537A-3ED3-E29A-DD00",
    "Pool Party": "FFF6-E7FF-F6E7-FC00",
    "Champion": "3F3F-46D0-DFDE-E800",
    "Steampunk": "A25D-3430-DAA5-C200",
    "Ranked": "FFCC-00E4-E4F0-F700",
}

ori = {
    "Default": "F8F5-FCF8-F5FC-0000-005D-CBF1-FFC8-21A4",
    "Cyan": "C3E9-F8C3-E9F8-0000-009D-51D5-5C7D-C45B",
    "Red": "EFCA-CAEF-CACA-0000-00FF-DC72-F77D-7DF5",
    "Green": "DAF9-E2DA-F9E2-0000-00F7-9385-4A9B-5B47",
    "Dark": "4354-8443-5484-C7FF-35C7-FF35-DDE2-F41D",
    "Pink": "F1C5-F3F9-F6FB-0000-00DE-AAFF-5BFF-BFBE",
    "Christmas": "EF34-0FFF-FCFC-0000-006D-FF53-FF86-803A",
    "Valentines": "FFFF-FFFF-99D2-0000-00E3-4B4B-B700-702F",
    "Summer": "FFF6-8CFF-A628-0000-0059-CDE9-FFFD-E55E",
    "Halloween": "413E-3741-3E37-EBDD-00CE-902F-EBDD-001A",
    "Default Custom 1": "EA00-0000-157F-4A12-7177-8194-F0F6-440D",
    "Default Custom 2": "872C-2CFF-DEB3-4399-8CF3-BFBF-4399-8C2A",
    "Infamous": "5552-AA37-E9FF-D445-FE00-FFA8-D445-FE35",
    "Champion": "3F3F-46D0-DFDE-0000-00B2-FFD0-5252-52CB",
    "Abyss": "4E3D-5D4E-3D5D-FF7F-00DC-71FF-FF7F-0093",
    "Early Access": "D3E2-9AD3-E29A-0000-0052-7A3E-A7B9-4ADE",
    "Ranked": "FFCC-00E4-E4F0-0000-00FF-8700-BE57-2383",
}

pomme = {
    "Blue": "BED2-E923-4160-1550-5810-1574-65B8-9C87-E7D1-1A00",
    "Red": "E9BE-CA6C-1B2E-3320-1974-101E-B897-65E2-CE7F-D500",
    "Green": "CDEE-E242-6C1B-0834-3A10-7469-747A-BF97-9FF7-2700",
    "White": "EAE6-EE3D-384F-4950-6213-2837-AEAF-CE93-9BB4-2200",
    "Purple": "D7C5-FF32-2347-1611-272A-083D-6840-8AC1-8FFF-3700",
    "Christmas": "F4DE-DE3B-AE38-FB00-008C-4848-AD0F-389A-A0FE-E200",
    "Valentines": "F4BB-DDBB-2243-FB62-C3CD-5555-AD3F-97FE-59CE-A700",
    "Summer": "F4E0-9056-D3F0-FF92-1742-BAB3-F886-435D-B5EE-7300",
    "Halloween": "9482-53BE-1414-621B-0D00-0000-332D-29E6-AE4D-5200",
    "Default Custom 1": "E8D9-D366-4917-7F81-8287-5100-D6D6-D6E0-BE8B-C400",
    "Default Custom 2": "CEBB-BB35-2A2A-5100-0040-0000-9129-29ED-9B87-2500",
    "Abyss": "5654-9291-3BCE-4F3D-5E4E-178D-A6AC-D6F4-D4FF-EF00",
    "Early Access": "D3E2-9A53-7A3E-2343-3123-4331-A7BA-4AD3-E29A-3900",
    "Ranked": "FAEF-D3FF-EC52-FFB5-47FF-9403-9C5F-A0DD-CE00-3700",
}

ranno = {
    "Blue": "712F-DF10-0060-A532-32BB-9992-A5A1-FFB6",
    "Red": "E86A-6A61-0000-A532-32D3-C797-FFA3-A358",
    "Green": "B0CD-5728-4B52-3977-9AB3-B5BB-00CA-69E7",
    "Grey": "F7F7-F739-3939-1F1F-1FFF-FFFF-9F9F-9F1A",
    "Pink": "E84C-C570-0348-5EAA-70BE-AD9D-DCFF-E43F",
    "Christmas": "AFFF-A900-9712-CF00-00FF-FFFF-FFFF-FF85",
    "Valentines": "FFD3-D3FF-99D2-E34B-4BFF-D9ED-B700-7035",
    "Summer": "FFF6-8CC0-8A4F-59CC-E9FF-FDE5-FFA6-288B",
    "Halloween": "E9E9-E91C-1D1E-7373-7386-1B1B-E800-0086",
    "Default Custom 1": "3B49-87CD-F7F7-0000-00BF-C2F3-FFA7-491D",
    "Default Custom 2": "872C-2CFF-DEB3-4399-8CF3-BFBF-4399-8C2A",
    "Pool Party": "F790-0E71-2500-F86E-6EC1-C19B-85EF-FE60",
    "Champion": "C9C9-DC3F-3F46-B2FF-D0D2-D2B4-FFFF-FEA1",
    "Abyss": "A6AC-D64F-3D5E-4E17-8D92-3BCE-DC71-FF4E",
    "Early Access": "537A-3ED3-E29A-D3E2-9AA7-BA4A-537A-3EFB",
    "Golden": "FFF7-CAFF-DD1E-FFDD-1EFF-DD1E-FEFF-0533",
    "Infamous": "37EA-FF33-3741-5653-AAD4-45FE-00FF-A8D6",
    "Ranked": "E4E4-F079-7AC3-FFCC-00FF-8700-F2FD-FFE9",
}

shovel_knight = {
    "Cyan": "B2F0-DC4D-380B-9F9D-60FA-FFFF-EA00",
    "Red": "CE48-2856-443C-FFFF-00C2-A996-7C00",
    "Green": "52B7-4E04-5300-FFFF-00ED-D9B7-E300",
    "Dark": "6A6A-6A29-2929-DE2A-12E6-6756-4000",
    "Purple": "9B7E-DE7C-0E73-E679-83E8-B1A6-7100",
    "Christmas": "FF22-2232-B50F-FFFF-FFFF-FFFF-3900",
    "Valentines": "FF99-D2B7-0070-E34B-4BFF-F3FB-3A00",
    "Summer": "FFF6-8C59-CCE9-4592-72FF-A628-3800",
    "Halloween": "BD00-0057-5757-D190-3BFF-EDB3-4900",
    "Default Custom 1": "DE6C-2561-3131-B466-3B46-1B00-5800",
    "Default Custom 2": "FFFF-FF61-83A5-BDAA-D52C-1B4E-E800",
    "Golden": "FCD5-3575-5C00-FCFC-FCFF-FFFE-BA00",
    "Infamous": "00FF-A856-53AA-D445-FE37-EAFF-5500",
    "Abyss": "5654-924F-3D5E-DC71-FFA6-ACD6-F400",
    "Early Access": "537A-3ED3-E29A-D3E2-9AA7-BA4A-8200",
    "Champion": "6A6A-6A41-3F37-B2FF-D0D0-DFDE-B400",
    "Ranked": "FFCC-0079-7AC3-FF87-00E4-E4F0-5C00",
}

sylvanos = {
    "Blue": "3B3B-758B-D5FF-807A-76BC-D5FF-FFFF-FF14",
    "Red": "7529-29FF-9566-9B6E-6ED0-1515-FFC1-55FD",
    "Green": "2F87-65B9-FF8E-859F-79EF-FF83-FFAC-AC53",
    "White": "3D3D-3DFF-FFFF-9393-93D9-5775-FFFF-FFE8",
    "Purple": "5D34-60B1-8EFF-9D85-9FFF-83CC-7750-6950",
    "Christmas": "FFFF-FF69-BA4A-E836-36FF-FFFF-FF3E-3EEA",
    "Valentines": "FFFF-FFFF-99D2-FFD9-EDB7-0070-E34B-4B77",
    "Summer": "FFF6-8CFF-A628-59CC-E959-CCE9-FFFD-E535",
    "Halloween": "1A3D-56AD-FF91-9CAB-92B1-41D6-E58A-E8ED",
    "Default Custom 1": "FFAE-445F-554C-CBB6-B6FF-F4E0-5D56-569A",
    "Default Custom 2": "79AD-6488-685D-D5D8-DD3C-2424-79AD-64EA",
    "Genesis": "3435-379E-2317-FAF7-F7FF-3941-FF39-41A0",
    "Infamous": "3337-4100-FFA8-5653-AAD4-45FE-37EA-FFB6",
    "Abyss": "4F3D-5EDC-71FF-5654-92A6-ACD6-903B-CECE",
    "Early Access": "2343-31A7-BA4A-537A-3ED3-E29A-A7BA-4AAA",
    "Golden": "FFDD-1EFF-E762-FFDD-1EFF-DD1E-FFF6-CF66",
    "Champion": "3F3F-46B2-FFD0-C9C9-DCD0-DFDE-B2FF-D052",
    "Ranked": "FFCC-00FF-8700-E4E4-F0FF-F4E0-FF87-0083",
    "Steampunk": "5252-52A2-5D34-30DA-A58A-8A8A-FFFF-FF38",
}

wrastor = {
    "Blue": "4194-D41F-4579-B8DF-FFBE-F4FF-E6DA-194C",
    "Red": "C549-4678-2F33-FFC0-BEEB-C375-E6DA-19E3",
    "Green": "57A8-643D-5A3E-C1FF-CAED-F7A7-E6DA-1916",
    "Grey": "7677-793E-3E40-FFFF-FFFF-FFFF-E6DA-19E7",
    "Purple": "645E-B07B-3329-FEFC-D3D3-BCF3-E6DA-1983",
    "Christmas": "DE48-484E-7F25-7DEC-5BFF-FFFF-FFFF-FF78",
    "Valentines": "FFEC-F7E3-4B4B-FF93-C6FF-ECF7-F8FF-90CA",
    "Summer": "59CC-E945-9272-FFA6-28C9-F5FF-FFF6-8CD3",
    "Halloween": "F692-1D61-5645-A73E-85F6-D5AD-E6DA-1917",
    "Default Custom 1": "3939-31AD-3131-CE7B-29C6-B573-FFC6-5A9E",
    "Default Custom 2": "FFFF-FFEF-5A9C-FAD8-5AFF-C6CF-E6DA-196F",
    "Spangled": "B222-343C-3B6E-FFFF-FFFF-FFFF-E6DA-19A1",
    "Champion": "2926-21FF-FFFF-B2FF-D058-544E-9692-8CE7",
    "Abyss": "5654-924F-3D5E-DC71-FFA6-ACD6-A6AC-D6B4",
    "Early Access": "A7BA-4A53-7A3E-D3E2-9AD3-E29A-D3E2-9AA7",
    "Collegiate": "324D-BBFF-CA07-F7FC-FFC0-DAFF-FFCA-07DD",
    "Golden": "FFDD-1EFC-D535-FCFC-FCFF-F7CA-FFF2-AB4D",
    "Ranked": "E4E4-F0FF-CC00-FF87-00F9-E1BE-FFD8-3D1E",
}

zetterburn = {
    "Blue": "4B5F-C0FA-FDFF-A9FF-DA3F-B1EB-0030-77CD",
    "Red": "CE30-30FD-F724-FFBA-87FF-5F5F-A001-2A8A",
    "Green": "237A-35BD-FFA6-D2FF-001F-DD00-007F-0F43",
    "Grey": "393A-3CFF-FFFF-D5D6-D983-8588-4040-412C",
    "Purple": "FAFD-FFDC-CB69-9D87-C36F-5EA6-3C30-3CF6",
    "Christmas": "DE48-48FD-F4AB-FFFF-FFFD-E5E7-EDC4-BE9A",
    "Valentines": "FF95-D3FF-D9ED-FFAC-FEF7-4CD5-D700-8EF5",
    "Summer": "59CC-E9FF-F68C-FFD8-A1FF-A628-AC51-004E",
    "Halloween": "6156-45FF-DEB8-FF7D-00A7-3E85-7729-5D59",
    "Default Custom 1": "FA94-0CDC-B97F-FFFF-3CF7-C00A-EB88-00D9",
    "Default Custom 2": "2C3A-6D9C-6E69-3C3C-3C23-2323-0C0C-0C7E",
    "Champion": "5252-5252-5252-FFFF-FFD0-DFDE-D0DF-DE19",
    "Excaliburn": "3C36-20A9-2E2E-1306-0413-0604-B635-35E6",
    "Abyss": "4F3D-5EA6-ACD6-DC71-FF92-3BCE-4E17-8DD8",
    "Early Access": "537A-3ED3-E29A-D3E2-9AA7-BA4A-537A-3EFB",
    "Shine": "DCCB-69E5-E1AF-A0FF-FF22-A5E7-FFF9-F940",
    "Golden": "F1CC-3FF0-D94F-FFFF-FFFD-FFFC-FFF8-C46F",
    "Ranked": "FFCC-00F9-E1BE-FFD8-3DE4-E4F0-0000-00B2",
    "Steampunk": "5252-52E4-923F-30D9-A312-9477-0257-552E",
}

if __name__ == "__main__":
    # initializes Chrome driver with the desired options
    driver = start_headless_driver()

    create_named_recolors(driver, "Ori", ori)
    # generate_recolors_sequence(driver, recolors, custom_skins_dir)

    # closing browser
    driver.close()
