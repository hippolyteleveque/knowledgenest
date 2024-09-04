import { sendActiveUrl, checkTokenValidity } from "./lib.js";

chrome.action.onClicked.addListener(handleActionClick);

function handleActionClick(tab) {
  chrome.storage.sync.get(
    ["kn-jwtToken", "kn-token-exp"],
    async function (data) {
      if (
        data["kn-jwtToken"] &&
        data["kn-token-exp"] &&
        checkTokenValidity(data["kn-token-exp"])
      ) {
        const resp = await sendActiveUrl(data["kn-jwtToken"]);
        // Remove popup to allow future clicks to trigger the listener
        if (resp.ok) {
          chrome.action.setPopup({ popup: "success-popup.html" });
          chrome.action.openPopup();
        } else {
          chrome.action.setPopup({ popup: "failure-popup.html" });
          chrome.action.openPopup();
        }
      } else {
        chrome.action.setPopup({ popup: "login-popup.html" });
        chrome.action.openPopup();
      }
    }
  );
}
