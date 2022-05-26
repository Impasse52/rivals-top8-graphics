import styled from "styled-components";

export const CharacterSelectionContainer = styled.div`
  position: relative;
`;

export const CharacterButton = styled.div`
  width: 49px;
  height: 49px;
  padding: 5px;
  margin: 2px;
  border: 0;
  border-radius: 35px;
  background-color: white;

  &:hover {
    color: black;
    background-color: rgb(72, 114, 162);
    transition: 0.2s;
    color: white;
    box-shadow: inset 0px 5px 0px 0px rgb(60, 95, 132);
  }

  &:active {
    background-color: rgb(188, 188, 188);
    transition: 0.2s;
  }
`;

export const SelectedCharacter = styled.img`
  width: 49px;
  height: 49px;
  image-rendering: crisp-edges;
`;

export const CharacterPicker = styled.div`
  position: absolute;
  z-index: 1;
  display: flex;
  border-radius: 35px;
  width: 320px;
  height: fit-content;
  background-color: rgb(233, 233, 233);
  padding: 10px;

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  animation: 0.1s ease-out 0s 1 fadeIn;

`;

export const CharacterIconRow = styled.div`
  display: table-row;
`;

export const CharacterIcon = styled.img`
  width: 49px;
  height: 49px;
  padding: 5px;
  margin: 2px;
  border-radius: 25px;
  image-rendering: crisp-edges;

  &:hover {
    background-color: rgb(208, 208, 208);
    transition: 0.2s;
  }
`;

export const CharacterIconCell = styled.div`
  display: table-cell;
  border-radius: 35px;
`;
