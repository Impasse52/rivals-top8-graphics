import {
  BackgroundsList,
  TournamentMeta,
  TournamentSettings,
} from "../../types";
import { InputField, Label } from "../PlacementInput/styles";
import BackgroundSelect from "../BackgroundSelect";
import { InputCell, InputRow, TournamentInputContainer } from "./styles";
import BGSelectVariant from "../BGSelectVariant";

function hexToRgb(hex_color: string) {
  const color = hex_color.substring(1, 8);
  const r = Number.parseInt(color.substring(0, 2), 16);
  const g = Number.parseInt(color.substring(2, 4), 16);
  const b = Number.parseInt(color.substring(4, 6), 16);

  return [r, g, b];
}

function rgbToHex(rgb: number[]) {
  var r = rgb[0].toString(16);
  var g = rgb[1].toString(16);
  var b = rgb[2].toString(16);

  if (r.length === 1) r = "0" + r;
  if (g.length === 1) g = "0" + g;
  if (b.length === 1) b = "0" + b;

  return `#${r}${g}${b}`;
}

export default function TournamentInput(props: {
  meta: TournamentMeta;
  setMeta: CallableFunction;
  settings: TournamentSettings;
  setSettings: CallableFunction;
  backgroundsList: BackgroundsList;
}) {
  const { meta, setMeta, settings, setSettings, backgroundsList } = props;

  return (
    <TournamentInputContainer>
      <InputRow style={{ gridTemplateColumns: "3.5fr 1fr" }}>
        <InputCell>
          <Label>Tournament name</Label>
          <InputField
            type="text"
            placeholder="Tournament name"
            value={meta.title}
            onChange={(e) => setMeta({ ...meta, title: e.target.value })}
          />
        </InputCell>

        <InputCell>
          <Label>Attendees</Label>
          <InputField
            type="number"
            placeholder="Attendees number"
            value={meta.participants}
            onChange={(e) => setMeta({ ...meta, participants: e.target.value })}
          />
        </InputCell>
      </InputRow>
      <InputRow style={{ gridTemplateColumns: "1fr" }}>
        <InputCell>
          <Label>Date</Label>
          <InputField
            type="date"
            placeholder="Date"
            value={meta.date}
            onChange={(e) => setMeta({ ...meta, date: e.target.value })}
          />
        </InputCell>
      </InputRow>
      <InputRow style={{ gridTemplateColumns: "0.5fr 2.5fr 0.5fr" }}>
        <InputCell>
          <Label>RGB</Label>
          <InputField
            type="color"
            placeholder="RGB"
            value={rgbToHex(settings.rgb)}
            onChange={(e) => {
              setSettings({ ...settings, rgb: hexToRgb(e.target.value) });
            }}
          />
        </InputCell>
        <InputCell>
          <Label>Background</Label>
          <BackgroundSelect
            type="background"
            options={Object.keys(backgroundsList)}
            meta={meta}
            setMeta={setMeta}
          />
        </InputCell>
        <InputCell>
          <Label>Variant</Label>
          <BGSelectVariant
            type="background_variant"
            number={backgroundsList[meta.background] ?? [1]}
            meta={meta}
            setMeta={setMeta}
          />
        </InputCell>
      </InputRow>
    </TournamentInputContainer>
  );
}
