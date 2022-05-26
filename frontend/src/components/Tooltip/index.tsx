import { TooltipContainer } from "./styles";

export function Tooltip(props: { id: string | undefined; tip: string }) {
  const { id, tip } = props;

  return (
    <TooltipContainer id={id} title={tip} style={{ marginInline: "15px" }}>
      &#x1F6C8;
    </TooltipContainer>
  );
}
