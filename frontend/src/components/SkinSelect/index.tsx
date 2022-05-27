import { v4 } from "uuid";
import {
  CustomSkinsCheckbox,
  SkinSelectContainer,
  StyledSelect,
  StyledTextinput,
} from "./styles";

export default function SkinSelect(props: {
  skinsList: string[];
  customSkinsList: any[];
  skin: string;
  setSkin: CallableFunction;
  customSkinsEnabled: boolean;
  enableCustomSkins: CallableFunction;
}) {
  const {
    customSkinsEnabled,
    enableCustomSkins,
    skin,
    setSkin,
    skinsList,
    customSkinsList,
  } = props;

  return (
    <SkinSelectContainer>
      {!customSkinsEnabled ? (
        <StyledSelect onChange={(e) => setSkin(e.target.value)} value={skin}>
          {skinsList.map((o: any) => (
            <option value={o} key={v4()}>
              {o}
            </option>
          ))}
          {Object.keys(customSkinsList).map((o: any) => (
            <option value={customSkinsList[o]} key={v4()}>
              {o}
            </option>
          ))}
        </StyledSelect>
      ) : (
        <StyledTextinput
          type="text"
          placeholder="Custom skin code"
          value={skin}
          onChange={(e) => setSkin(e.target.value)}
        />
      )}
      {/* using a hack to render a round "checkbox" with no errors nor warnings */}
      <CustomSkinsCheckbox
        type="radio"
        style={{height: "34px"}}
        checked={customSkinsEnabled}
        onChange={() => enableCustomSkins(!customSkinsEnabled)}
        onClick={() => enableCustomSkins(!customSkinsEnabled)}
      ></CustomSkinsCheckbox>
    </SkinSelectContainer>
  );
}
