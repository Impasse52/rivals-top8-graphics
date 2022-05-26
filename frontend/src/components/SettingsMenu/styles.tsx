import styled from "styled-components";

export const SettingsMenuContainer = styled.div`
  position: relative;
`;

export const SettingsButton = styled.input`
  font-family: "Material Icons";
  font-size: 40px;
  color: white;
  border-radius: 35px;
  border: 0;
  background-color: transparent;
  display: flex;
  margin-left: auto;

  &:hover {
    background-color: rgb(208, 208, 208, 0.3);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(188, 188, 188);
    transition: 0.2s;
  }
`;

export const SettingsList = styled.div`
  position: absolute;
  right: 0px;
  z-index: 1;
  display: flex;
  flex-direction: column;
  border-radius: 35px;
  width: 320px;
  height: fit-content;
  background-color: rgb(233, 233, 233);
  transition: 0.2s;
  padding: 10px;
  margin-block: 3px;

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

export const SettingsItem = styled.div`
  margin: 20px;
`;

export const ItemContent = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;

  & > * {
    height: 40px;
  }
`;

export const InputField = styled.input`
  border: 1px solid rgb(208, 208, 208);
  border-radius: 35px;
  text-align: center;
  font-size: 18px;
  background-color: white;
  box-sizing: border-box;
  width: 100%;

  &:hover {
    background-color: rgb(208, 208, 208);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(188, 188, 188);
    transition: 0.2s;
  }
`;

export const FetchButton = styled.input`
  border: 0;
  background-color: rgb(208, 208, 208);
  border: 1px solid white;
  border-radius: 35px;
  font-size: 15px;
  width: 80px;
  margin-inline: 5px;

  &:hover {
    background-color: rgb(255, 255, 255, 0.6);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(255, 255, 255);
    transition: 0.2s;
  }
`;

export const Credits = styled.div`
  margin: 5px;
  display: inline;

  & > a {
    color: black;
    display: inline;
    margin: 4px;
  }

  & > a:hover {
    transition: 0.2s;
    color: gray;
  }
`;
