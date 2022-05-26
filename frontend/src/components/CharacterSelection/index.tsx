import { useCallback, useEffect, useState } from "react";
import { v4 } from "uuid";
import { CharactersList } from "../../types";
import {
  CharacterButton,
  CharacterIcon,
  CharacterIconCell,
  CharacterIconRow,
  CharacterSelectionContainer,
  CharacterPicker,
  SelectedCharacter,
} from "./styles";

export default function CharacterSelection(props: {
  charactersList: CharactersList;
  assetsDir: string;
  type: string;
  setCharacter: CallableFunction;
  character: String;
}) {
  const { character, setCharacter, charactersList, assetsDir, type } = props;

  const [showList, setShowList] = useState(false);

  // using useCallback to properly remove the eventListener
  const clickOutsideMenu = useCallback((e: any) => {
    if (
      (e.target as HTMLElement).id !== "charactersList" &&
      (e.target as HTMLElement).id !== "characterIcon"
    ) {
      setShowList(false);
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

  return (
    <CharacterSelectionContainer>
      <CharacterButton
        id="characterButton"
        onClick={() => handleShowingList()}
        tabIndex={1}
        onContextMenu={(e) => {
          e.preventDefault();
          setCharacter("None");
        }}
      >
        <SelectedCharacter src={`${assetsDir}/${character}.png`} />
      </CharacterButton>
      {showList ? (
        <CharacterPicker id="charactersList">
          <CharacterIconRow>
            <CharacterIconCell>
              {charactersList.characters.map((char) => (
                <CharacterIcon
                  id="characterIcon"
                  src={`${assetsDir}/${char}.png`}
                  alt={`${assetsDir}/${char}.png`}
                  onClick={() => {
                    setCharacter(char);
                    setShowList(false);
                  }}
                  key={v4()}
                />
              ))}
            </CharacterIconCell>
          </CharacterIconRow>
        </CharacterPicker>
      ) : (
        <></>
      )}
    </CharacterSelectionContainer>
  );
}
