import { sendActiveUrl } from "./lib.js";

chrome.action.onClicked.addListener(handleActionClick);

function handleActionClick(tab) {
  chrome.storage.sync.get("kn-jwtToken", function (data) {
    if (data["kn-jwtToken"]) {
      sendActiveUrl(data["kn-jwtToken"]);
      // Remove popup to allow future clicks to trigger the listener
      chrome.action.setPopup({ popup: "" });
    } else {
      chrome.action.setPopup({ popup: "popup.html" });
      chrome.action.openPopup();
    }
  });
}
