import { useState } from "react";
import { skinsListSample } from "../../api";
import { InputField, Button, UploadFileContainer, LinkButton } from "./styles";

export function UploadFileButton(props: { filename: string }) {
  const [filename, setFilename] = useState<string>(props.filename);

  function handleUpload(e: any) {
    const fileReader = new FileReader();
    fileReader.readAsText(e.target.files[0], "UTF-8");

    const skinsFilename = e.target!.files[0].name;
    setFilename(skinsFilename);

    fileReader.onload = (e) => {
      const skins = e.target!.result as string;
      localStorage.setItem("skins", skins);
      localStorage.setItem("skins_filename", skinsFilename);
    };

    // ? temp: can't re-render after uploading a file for some reason
    // eslint-disable-next-line no-restricted-globals
    location.reload();
  }

  function downloadSample() {
    return `data:text/json;charset=utf-8,${encodeURIComponent(
      JSON.stringify(skinsListSample)
    )}`;
  }

  return (
    <UploadFileContainer>
      <input
        id="uploadButton"
        type="file"
        onChange={(e) => handleUpload(e)}
        hidden
      />
      <LinkButton href={downloadSample()} download="skinslist_sample.json">
        Sample
      </LinkButton>
      <Button htmlFor="uploadButton">Upload</Button>
      <InputField
        disabled
        value={filename ? filename : "No file has been selected."}
      />
    </UploadFileContainer>
  );
}
