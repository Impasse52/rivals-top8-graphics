export default function Preview(props: { src: string; loading: boolean }) {
  const { src, loading } = props;
  const style = {
    filter: "blur(4px)",
  };

  return (
    <img src={src} alt="Preview" height="95%" style={loading ? style : {}} />
  );
}
