import styled from "styled-components";

export const UploadFileContainer = styled.div`
  display: flex;
`;

export const LinkButton = styled.a`
  color: black;
  text-decoration: none;
  display: flex;
  border: 0;
  background-color: rgb(208, 208, 208);
  border: 1px solid white;
  border-radius: 35px;
  font-size: 13px;
  margin-inline: 1px;
  padding: 2px;
  height: 35px;
  width: 90px;
  align-items: center;
  text-align: center;
  justify-content: center;

  &:hover {
    background-color: rgb(255, 255, 255, 0.6);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(255, 255, 255);
    transition: 0.2s;
  }`;

export const Button = styled.label`
  display: flex;
  border: 0;
  background-color: rgb(208, 208, 208);
  border: 1px solid white;
  border-radius: 35px;
  font-size: 13px;
  margin-inline: 1px;
  padding: 2px;
  height: 35px;
  width: 90px;
  align-items: center;
  text-align: center;
  justify-content: center;

  &:hover {
    background-color: rgb(255, 255, 255, 0.6);
    transition: 0.2s;
  }

  &:active {
    background-color: rgb(255, 255, 255);
    transition: 0.2s;
  }
`;

export const InputField = styled.input`
  border: 1px solid rgb(208, 208, 208);
  border-radius: 35px;
  text-align: center;
  font-size: 12px;
  background-color: white;
  box-sizing: border-box;
  width: 100%;
`;
