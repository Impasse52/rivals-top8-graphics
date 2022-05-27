import { useCallback, useEffect, useState } from "react";
import { TournamentSettings } from "../../types";
import { Label } from "../PlacementInput/styles";
import { Tooltip } from "../Tooltip";
import { UploadFileButton } from "../UploadFileButton";
import {
  SettingsMenuContainer,
  SettingsList,
  SettingsButton,
  SettingsItem,
  ItemContent,
  InputField,
  FetchButton,
  Credits,
} from "./styles";

export default function SettingsMenu(props: {
  settings: TournamentSettings;
  setSettings: CallableFunction;
  fetchBracket: CallableFunction;
}) {
  const { settings, setSettings, fetchBracket } = props;
  const [showList, setShowList] = useState(false);
  const [bracketUrl, setBracketUrl] = useState("");

  // using useCallback to properly remove the eventListener
  const clickOutsideMenu = useCallback((e: any) => {
    if (
      ![
        "settingsList",
        "fetchText",
        "fetchButton",
        "uploadJSON",
        "layout1",
        "layout2",
        "layout1_label",
        "layout2_label",
        "uploadFileButton",
      ].includes((e.target as HTMLElement).id)
    ) {
      // setShowList(false);
    }
  }, []);

  function handleShowingList() {
    setShowList(!showList);
    document.addEventListener("click", clickOutsideMenu, true);
  }

  // removes event listener from document object
  useEffect(() => {
    if (showList === false)
      document.removeEventListener("click", clickOutsideMenu, true);
  }, [showList, clickOutsideMenu]);

  const tip =
    "Import custom skin codes by uploading a JSON file, adding them to the skins list. The JSON must be structured exactly like the sample.";

  return (
    <SettingsMenuContainer>
      <SettingsButton
        id="characterButton"
        onClick={() => handleShowingList()}
        value={!showList ? "settings" : "cancel"}
        type="button"
      />
      {showList ? (
        <SettingsList id="settingsList">
          <SettingsItem id="settingsItem">
            <Label style={{ display: "flex" }}>
              Skins JSON
              <Tooltip id="tooltip" tip={tip} />
            </Label>
            <ItemContent>
              <div id="uploadFileButton">
                <UploadFileButton
                  filename={localStorage.getItem("skins_filename") ?? ""}
                />
              </div>
            </ItemContent>
          </SettingsItem>
          <SettingsItem>
            <Label>Layout</Label>
            <ItemContent>
              <div>
                <input
                  id="layout1"
                  type="radio"
                  defaultChecked={settings.layout === 1}
                  onClick={() => {
                    setSettings({ ...settings, layout: 1 });
                    setShowList(false);
                  }}
                />
                <label id="layout1_label" htmlFor="layout1">
                  Layout 1
                </label>
                <input
                  id="layout2"
                  type="radio"
                  defaultChecked={settings.layout === 2}
                  onClick={() => {
                    setSettings({ ...settings, layout: 2 });
                    setShowList(false);
                  }}
                />
                <label id="layout2_label" htmlFor="layout2">
                  Layout 2
                </label>
              </div>
            </ItemContent>
          </SettingsItem>
          <SettingsItem>
            <Label>Fetch tournament</Label>
            <ItemContent>
              <InputField
                id="fetchText"
                type="text"
                value={bracketUrl}
                onChange={(e) => setBracketUrl(e.target.value)}
              />
              <FetchButton
                id="fetchButton"
                type="button"
                value="Fetch"
                onClick={() => fetchBracket(bracketUrl)}
              />
            </ItemContent>
          </SettingsItem>
          <SettingsItem>
            <Label>Credits</Label>
            <ItemContent>
              <Credits>
                Thanks to
                <a
                  href="https://twitter.com/Readeku/"
                  target="_blank"
                  rel="noreferrer"
                >
                  Readek
                </a>
                for allowing me to use their custom skins tool in this project,
                to
                <a
                  href="https://twitter.com/Kaiwarete/"
                  target="_blank"
                  rel="noreferrer"
                >
                  Lucy
                </a>
                for testing this and to
                <a
                  href="https://twitter.com/kiirochii"
                  target="_blank"
                  rel="noreferrer"
                >
                  Kii
                </a>
                for providing the base graphic!
              </Credits>
            </ItemContent>
          </SettingsItem>
          <div style={{ margin: "15px" }}></div>
        </SettingsList>
      ) : (
        <></>
      )}
    </SettingsMenuContainer>
  );
}
