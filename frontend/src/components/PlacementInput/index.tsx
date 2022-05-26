import { BackgroundsList, CharactersList, CustomSkin, PlayerData } from "../../types";
import CharacterSelection from "../CharacterSelection";
import SkinSelect from "../SkinSelect";
import {
  Characters,
  InnerLabel,
  InputField,
  Label,
  PlacementContainer,
  Section,
} from "./styles";

export default function PlacementInput(props: {
  player_number: number;
  charactersList: CharactersList;
  skinsList: string[];
  customSkins: CustomSkin[];
  backgroundsList: BackgroundsList;
  assetsDir: string;
  playerData: PlayerData;
  setPlayerData: React.Dispatch<React.SetStateAction<PlayerData>>;
}) {
  const {
    player_number,
    playerData,
    setPlayerData,
    charactersList,
    skinsList,
    customSkins: customSkinsList,
    assetsDir,
  } = props;

  return (
    <PlacementContainer>
      <Section>
        <Label>Player {player_number}</Label>
        <InputField
          type="text"
          placeholder="Nickname"
          value={playerData.nickname}
          onChange={(e) =>
            setPlayerData({ ...playerData, nickname: e.target.value })
          }
        />
      </Section>
      <Section>
        <Label>
          Characters <InnerLabel>(right-click to remove!)</InnerLabel>
        </Label>
        <Characters>
          <CharacterSelection
            type="character"
            charactersList={charactersList}
            assetsDir={assetsDir}
            character={playerData.character}
            setCharacter={(c: string) =>
              setPlayerData({ ...playerData, character: c })
            }
          />
          <CharacterSelection
            type="secondary"
            charactersList={charactersList}
            assetsDir={assetsDir}
            character={playerData.secondary}
            setCharacter={(c: string) =>
              setPlayerData({ ...playerData, secondary: c })
            }
          />
          <CharacterSelection
            type="tertiary"
            charactersList={charactersList}
            assetsDir={assetsDir}
            character={playerData.tertiary}
            setCharacter={(c: string) =>
              setPlayerData({ ...playerData, tertiary: c })
            }
          />
        </Characters>
      </Section>
      <Section>
        <Label>
          Skin <InnerLabel>(check this for custom skins!)</InnerLabel>
        </Label>
        <SkinSelect
          skinsList={skinsList}
          customSkinsList={customSkinsList}
          skin={playerData.skin}
          setSkin={(s: string) => setPlayerData({ ...playerData, skin: s })}
          customSkinsEnabled={playerData.custom_skin}
          enableCustomSkins={(c: boolean) =>
            setPlayerData({ ...playerData, custom_skin: c })
          }
        />
      </Section>
    </PlacementContainer>
  );
}
