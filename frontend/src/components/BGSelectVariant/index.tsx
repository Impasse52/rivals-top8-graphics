import { v4 } from "uuid";
import { TournamentMeta } from "../../types";
import { SkinSelectContainer, StyledSelect } from "./styles";

export default function BGSelectVariant(props: {
  type: string;
  number: number;
  meta: TournamentMeta;
  setMeta: CallableFunction;
}) {
  const { type, number, meta, setMeta } = props;

  let variants = [];
  for (let i = 1; i <= number; i++) variants.push(i);

  return (
    <SkinSelectContainer>
      <StyledSelect
        value={meta["background_variant"]}
        onChange={(e) => setMeta({ ...meta, [type]: e.target.value })}
      >
        {variants.map((o: any) => (
          <option value={o} key={v4()}>
            {o}
          </option>
        ))}
      </StyledSelect>
    </SkinSelectContainer>
  );
}
