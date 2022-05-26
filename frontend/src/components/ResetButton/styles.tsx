import styled from "styled-components";

export const ResetMenuContainer = styled.div`
  position: relative;
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

export const ResetItems = styled.div`
  display: flex;
  flex-direction: column;
  width: fit-content;
  align-content: center;
  padding: 25px;
  position: absolute;
  right: 25px;
  top: -145px;
  z-index: 1;
  border-radius: 35px;
  height: fit-content;
  background-color: rgb(93, 142, 202);

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

export const ConfirmButton = styled.input`
  border: 0;
  background-color: rgb(255, 0, 0);
  border: 0px solid;
  border-radius: 35px;
  font-size: 15px;
  width: 200px;
  height: 35px;
  font-size: 17px;
  color: white;
  margin-block: 5px;

  &:hover {
    background-color: rgb(100, 0, 0, 1);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(255, 255, 255);
    transition: 0.2s;
  }
`;

export const CancelButton = styled.input`
  border: 0px solid;
  background-color: rgb(208, 208, 208);
  color: black;
  border-radius: 35px;
  font-size: 15px;
  width: 200px;
  height: 35px;
  font-size: 17px;
  margin-block: 5px;

  &:hover {
    background-color: rgb(255, 255, 255, 0.6);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(255, 255, 255);
    transition: 0.2s;
  }
`;
