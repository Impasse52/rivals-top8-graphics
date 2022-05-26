import { Social } from "../../types";
import { SocialDiv, SocialImg, SocialsContainer } from "./styles";

export default function SocialsBar(props: { socials: Social[] }) {
  return (
    <SocialsContainer>
      {props.socials.map((s) => (
        <SocialDiv>
          <a href={s.url}>
            <SocialImg src={s.imageUrl} alt={s.name} style={s.style} />
          </a>
        </SocialDiv>
      ))}
    </SocialsContainer>
  );
}
