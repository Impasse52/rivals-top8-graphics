import { v4 } from "uuid";
import { TournamentMeta } from "../../types";
import { SkinSelectContainer, StyledSelect } from "./styles";

export default function BackgroundSelect(props: {
  type: string;
  options: any;
  meta: TournamentMeta;
  setMeta: CallableFunction;
}) {
  const { type, options, meta, setMeta } = props;

  return (
    <SkinSelectContainer>
      <StyledSelect
        value={meta["background"]}
        onChange={(e) => setMeta({ ...meta, [type]: e.target.value })}
      >
        <option value="Background">Background</option>
        {options.map((o: any) => (
          <option value={o} key={v4()}>
            {o}
          </option>
        ))}
      </StyledSelect>
    </SkinSelectContainer>
  );
}
