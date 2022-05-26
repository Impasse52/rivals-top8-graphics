import styled from "styled-components";

export const HomeContainer = styled.div`
  display: flex;
  flex-direction: column;

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  animation: 0.3s ease-out 0s 1 fadeIn;
`;

export const GeneratorContainer = styled.div`
  display: flex;
  flex-direction: row;
  margin: 15px;
  margin-inline: 200px;

  @media (max-width: 800px) {
    flex-direction: column;
    margin: 0px;
    margin-inline: 0px;
  }
`;

export const PlacementsContainer = styled.div`
  min-width: 65%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
`;

export const Settings = styled.div`
  display: flex;
`;

export const TournamentDataContainer = styled.div`
  min-width: 35%;
`;

export const PreviewContainer = styled.div`
  display: flex;
  text-align: center;
  align-content: center;
  justify-content: space-between;
  background-color: rgba(95, 151, 213, 0.8);
  border-radius: 35px;
  margin: 8px;
  padding: 6px;
  height: 265px;
  border-right: 5px solid #00000055;
  border-bottom: 5px solid #00000055;

  & > img {
    margin: auto;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
`;

export const HeaderContainer = styled.div`
  display: flex;
  margin: 15px;
  margin-inline: 210px;
  margin-top: 30px;
  justify-content: space-between;

  @media (max-width: 800px) {
    flex-direction: column;
    margin: 20px;
    margin-inline: 0px;
    text-align: center;
  }
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

export const Logo = styled.div`
  font-size: 40px;
  color: white;
`;

export const ButtonsContainer = styled.div`
  display: flex;
  margin: 15px;
  margin-inline: 200px;
  justify-content: center;
`;

export const Button = styled.input`
  border: 0;
  height: 50px;
  background-color: rgb(95, 151, 213);
  border-radius: 35px;
  padding: 10px;
  margin-inline: 50px;
  width: 200px;
  font-size: 18px;
  color: black;

  &:hover {
    color: black;
    background-color: rgb(72, 114, 162);
    border-top: 7px solid rgb(95, 151, 213);
    transition: 0.2s;
    color: white;
  }

  &:active {
    background-color: rgb(188, 188, 188);
    transition: 0.2s;
  }
`;
