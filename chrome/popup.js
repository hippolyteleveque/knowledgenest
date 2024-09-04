document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    chrome.action.setPopup({ popup: "" });
    window.close();
  }, 3000);
});


