import { useEffect, useState } from "react";
import "@fontsource/material-icons";
import PlacementInput from "../../components/PlacementInput";
import Preview from "../../components/Preview";
import TournamentInput from "../../components/TournamentInput";
import {
  BackgroundsList,
  CharactersList,
  CustomSkinsList,
  PlayerData,
  SkinsList,
  Social,
  TournamentMeta,
  TournamentSettings,
} from "../../types";

import {
  Button,
  ButtonsContainer,
  GeneratorContainer,
  HeaderContainer,
  HomeContainer,
  Logo,
  PlacementsContainer,
  PreviewContainer,
  Settings,
  TournamentDataContainer,
} from "./styles";
import SettingsMenu from "../../components/SettingsMenu";
import ResetButton from "../../components/ResetButton";
import {
  defaultSkinList,
  defaultPlayerData,
  defaultSettings,
  defaultTournamentData,
  generateTop8,
  getAllBackgrounds,
  getAllSkins,
  defaultBackgrounds as defaultBGs,
  assetsDir,
  getAllCharacters,
  defaultChars,
  defaultCustoms,
  fetchBracket,
} from "../../api";
import SocialsBar from "../../components/SocialsBar";

export default function Home() {
  // player data state
  const [player1, setPlayer1] = useState<PlayerData>(defaultPlayerData);
  const [player2, setPlayer2] = useState<PlayerData>(defaultPlayerData);
  const [player3, setPlayer3] = useState<PlayerData>(defaultPlayerData);
  const [player4, setPlayer4] = useState<PlayerData>(defaultPlayerData);
  const [player5, setPlayer5] = useState<PlayerData>(defaultPlayerData);
  const [player6, setPlayer6] = useState<PlayerData>(defaultPlayerData);
  const [player7, setPlayer7] = useState<PlayerData>(defaultPlayerData);
  const [player8, setPlayer8] = useState<PlayerData>(defaultPlayerData);

  // tournament metadata and settings state
  const [meta, setMeta] = useState<TournamentMeta>(defaultTournamentData);
  const [settings, setSettings] = useState<TournamentSettings>(defaultSettings);

  // api calls state
  const [outputURL, setOutputURL] = useState("/static/Resources/preview.png");
  const [skinsList, setSkinsList] = useState<SkinsList>(defaultSkinList);
  const [customSkins, setCustomSkins] =
    useState<CustomSkinsList>(defaultCustoms);
  const [backgrounds, setBackgrounds] = useState<BackgroundsList>(defaultBGs);
  const [characters, setCharacters] = useState<CharactersList>(defaultChars);
  const [loading, setLoading] = useState<boolean>(false);

  // decorates the generate function to easily pass it around along with its params
  const generateGraphic = () =>
    generateTop8(
      player1,
      player2,
      player3,
      player4,
      player5,
      player6,
      player7,
      player8,
      meta,
      settings,
      setOutputURL,
      setLoading
    );

  function resetForms() {
    setPlayer1(defaultPlayerData);
    setPlayer2(defaultPlayerData);
    setPlayer3(defaultPlayerData);
    setPlayer4(defaultPlayerData);
    setPlayer5(defaultPlayerData);
    setPlayer6(defaultPlayerData);
    setPlayer7(defaultPlayerData);
    setPlayer8(defaultPlayerData);
    setMeta(defaultTournamentData);
    setSettings(defaultSettings);
  }

  // retrieves the last generated top8
  useEffect(() => {
    let last_top8 = localStorage.getItem("last_top8") ?? "";

    if (last_top8) {
      const last_top8_json = JSON.parse(last_top8);
      setPlayer1(last_top8_json[1]);
      setPlayer2(last_top8_json[2]);
      setPlayer3(last_top8_json[3]);
      setPlayer4(last_top8_json[4]);
      setPlayer5(last_top8_json[5]);
      setPlayer6(last_top8_json[6]);
      setPlayer7(last_top8_json[7]);
      setPlayer8(last_top8_json[8]);
      setMeta(last_top8_json.meta);
      setSettings(last_top8_json.settings);
    }

    // retrieves skins, backgrounds and characters from backend
    getAllSkins(setSkinsList);
    getAllBackgrounds(setBackgrounds);
    getAllCharacters(setCharacters);
  }, []);

  // adds custom skins to the skins list
  useEffect(() => {
    const skinsList = localStorage.getItem("skins") ?? "";
    if (skinsList) setCustomSkins(JSON.parse(skinsList));
  }, []);

  const socials: Social[] = [
    {
      name: "Ko-fi",
      url: "https://ko-fi.com/impasse52",
      imageUrl: "https://storage.ko-fi.com/cdn/kofi_stroke_cup.svg",
      style: { height: "45px", width: "45px" },
    },
    {
      name: "Twitter",
      url: "https://twitter.com/Impasse52",
      imageUrl: "https://img.icons8.com/color/344/twitter--v1.png",
      style: { height: "50px" },
    },
    {
      name: "Github",
      url: "https://github.com/Impasse52/roa-top-8-graphics-generator",
      imageUrl:
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/600px-Octicons-mark-github.svg.png?20180806170715/",
      style: { height: "40px" },
    },
  ];

  const fetch = (url: string) => {
    fetchBracket(
      url,
      player1,
      player2,
      player3,
      player4,
      player5,
      player6,
      player7,
      player8,
      meta,
      setPlayer1,
      setPlayer2,
      setPlayer3,
      setPlayer4,
      setPlayer5,
      setPlayer6,
      setPlayer7,
      setPlayer8,
      setMeta
    );
  };

  return (
    <HomeContainer>
      <HeaderContainer>
        <Logo>RoA Top 8 Generator</Logo>
        <Settings>
          <SocialsBar socials={socials} />
          <SettingsMenu
            settings={settings}
            setSettings={setSettings}
            fetchBracket={fetch}
          />
        </Settings>
      </HeaderContainer>
      <GeneratorContainer>
        <PlacementsContainer>
          <PlacementInput
            player_number={1}
            charactersList={characters}
            skinsList={skinsList[player1.character] ?? []}
            customSkins={customSkins[player1.character] ?? []}
            assetsDir={assetsDir}
            playerData={player1}
            setPlayerData={setPlayer1}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={2}
            charactersList={characters}
            skinsList={skinsList[player2.character] ?? []}
            customSkins={customSkins[player2.character] ?? []}
            assetsDir={assetsDir}
            playerData={player2}
            setPlayerData={setPlayer2}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={3}
            charactersList={characters}
            skinsList={skinsList[player3.character] ?? []}
            customSkins={customSkins[player3.character] ?? []}
            assetsDir={assetsDir}
            playerData={player3}
            setPlayerData={setPlayer3}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={4}
            charactersList={characters}
            skinsList={skinsList[player4.character] ?? []}
            customSkins={customSkins[player4.character] ?? []}
            assetsDir={assetsDir}
            playerData={player4}
            setPlayerData={setPlayer4}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={5}
            charactersList={characters}
            skinsList={skinsList[player5.character] ?? []}
            customSkins={customSkins[player5.character] ?? []}
            assetsDir={assetsDir}
            playerData={player5}
            setPlayerData={setPlayer5}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={6}
            charactersList={characters}
            skinsList={skinsList[player6.character] ?? []}
            customSkins={customSkins[player6.character] ?? []}
            assetsDir={assetsDir}
            playerData={player6}
            setPlayerData={setPlayer6}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={7}
            charactersList={characters}
            skinsList={skinsList[player7.character] ?? []}
            customSkins={customSkins[player7.character] ?? []}
            assetsDir={assetsDir}
            playerData={player7}
            setPlayerData={setPlayer7}
            backgroundsList={backgrounds}
          />
          <PlacementInput
            player_number={8}
            charactersList={characters}
            skinsList={skinsList[player8.character] ?? []}
            customSkins={customSkins[player8.character] ?? []}
            assetsDir={assetsDir}
            playerData={player8}
            setPlayerData={setPlayer8}
            backgroundsList={backgrounds}
          />
        </PlacementsContainer>
        <TournamentDataContainer>
          <PreviewContainer>
            <Preview src={outputURL} loading={loading} />
          </PreviewContainer>
          <TournamentInput
            meta={meta}
            setMeta={setMeta}
            settings={settings}
            setSettings={setSettings}
            backgroundsList={backgrounds}
          />
        </TournamentDataContainer>
      </GeneratorContainer>
      <ButtonsContainer>
        <ResetButton resetCallback={resetForms} />
        <Button type="button" value="Generate" onClick={generateGraphic} />
      </ButtonsContainer>
    </HomeContainer>
  );
}
