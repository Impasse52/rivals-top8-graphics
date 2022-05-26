import styled from "styled-components";

export const SocialsContainer = styled.div`
  display: flex;
  align-items: center;
  padding-right: 17px;
`;

export const SocialDiv = styled.div`
  padding-inline: 10px;
  margin-inline: 5px;
`;

export const SocialImg = styled.img`
  height: 50px;
  transition: 0.2s ease-in-out;
  -webkit-transition: 0.2s ease-in-out;

  filter: grayscale(0%) contrast(100%) brightness(255);
  -webkit-filter: grayscale(0%);
  -webkit-filter: contrast(100%);
  -webkit-filter: brightness(255);

  &:hover {
    filter: grayscale(100%) contrast(100%) brightness(100%);
    -webkit-filter: grayscale(100%);
    -webkit-filter: contrast(100%);
    -webkit-filter: brightness(100%);
  }
`;
