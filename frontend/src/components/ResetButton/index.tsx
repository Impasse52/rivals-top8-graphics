/* eslint-disable react/jsx-no-undef */
import { useCallback, useEffect, useState } from "react";
import {
  ResetMenuContainer,
  ResetItems,
  Button,
  CancelButton,
  ConfirmButton,
} from "./styles";

export default function ResetButton(props: {
  resetCallback: CallableFunction;
}) {
  const { resetCallback } = props;

  const [showList, setShowList] = useState(false);

  // using useCallback to properly remove the eventListener
  const clickOutsideMenu = useCallback((e: any) => {
    if (
      !["resetList", "confirmButton"].includes((e.target as HTMLElement).id)
    ) {
      setShowList(false);
    }
  }, []);

  function handleShowingList() {
    setShowList(!showList);
    document.addEventListener("click", clickOutsideMenu, true);
  }

  // removes event listener from document object
  useEffect(() => {
    if (showList === false)
      document.removeEventListener("click", clickOutsideMenu, true);
  }, [showList, clickOutsideMenu]);

  // handles char variable changes

  return (
    <ResetMenuContainer>
      <Button
        id="characterButton"
        onClick={() => handleShowingList()}
        value="Reset"
        type="button"
      />
      {showList ? (
        <ResetItems id="resetList">
          <ConfirmButton
            id="confirmButton"
            type="button"
            value="Confirm"
            onClick={() => {
              resetCallback();
              setShowList(false);
            }}
          />
          <CancelButton type="button" value="Cancel" />
        </ResetItems>
      ) : (
        <></>
      )}
    </ResetMenuContainer>
  );
}
