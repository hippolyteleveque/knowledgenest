// const API_HOST = "https://knowledgenest.xyz"
export const API_HOST = "http://localhost:8000";


export function login(formData) {
  fetch(`${API_HOST}/api/v1/auth/login`, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["access_token"]) {
        chrome.storage.sync.set({ "kn-jwtToken": data["access_token"] });
      } else {
        alert("Authentication failed");
      }
    })
    .then(() => {
      // Remove popup to allow future clicks to trigger bg listener
      chrome.action.setPopup({ popup: "" });
      // Close the popup windows
      window.close();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Authentication failed");
    });
}

export function sendActiveUrl(token) {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentUrl = tabs[0].url;
    fetch(`${API_HOST}/api/v1/articles/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ url: currentUrl }),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to send URL");
      });
  });
}
