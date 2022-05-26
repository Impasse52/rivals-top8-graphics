import styled from "styled-components";

export const TournamentInputContainer = styled.div`
  display: flex;
  flex-direction: column;
  background-color: rgba(95, 151, 213, 0.8);
  border-radius: 35px;
  margin: 8px;
  margin-block: 10px;
  padding: 8px;
  height: 265px;
  border-right: 5px solid #00000055;
  border-bottom: 5px solid #00000055;
`;

export const InputRow = styled.div`
  display: grid;
  grid-column-gap: 20px;
`;

export const InputCell = styled.div`
  display: flex;
  flex-direction: column;
  margin: 8px;
`;
