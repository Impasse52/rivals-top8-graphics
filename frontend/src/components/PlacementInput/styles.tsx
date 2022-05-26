import styled from "styled-components";

export const PlacementContainer = styled.div`
  margin: 8px;
  max-width: 22%;
  height: 265px;
  border-radius: 25px;
  background-color: rgba(95, 151, 213, 0.8);
  padding: 6px;
  display: flex;
  flex: 1 1 20%;
  flex-direction: column;
  justify-content: space-evenly;
  border-right: 5px solid #00000055;
  border-bottom: 5px solid #00000055;

  @media (max-width: 800px) {
    max-width: 100%;
    flex: 1 1 100%;
    padding: 6px;
  }
`;

export const InputField = styled.input`
  border: 0;
  padding: 6px;
  border-radius: 35px;
  text-align: center;
  font-size: 18px;
  margin: 2px;
  background-color: rgb(233, 233, 237);
  height: 36px;
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

export const Characters = styled.div`
  display: flex;
  justify-content: space-between;
`;

export const Section = styled.div`
  margin: 5px;
`;

export const Label = styled.div`
  font-size: 16px;
  margin-bottom: 3px;
`;

export const InnerLabel = styled.span`
  font-size: 12px;
  margin-bottom: 3px;
`;
