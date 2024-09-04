// const API_HOST = "https://knowledgenest.xyz"
export const API_HOST = "http://localhost:8000";

export async function login(formData) {
  try {
    const response = await fetch(`${API_HOST}/api/v1/auth/login`, {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (data["access_token"] && data["token_expiration_time"]) {
      console.log(data["token_expiration_time"]);
      chrome.storage.sync.set({
        "kn-jwtToken": data["access_token"],
        "kn-token-exp": data["token_expiration_time"],
      });

      // Remove popup to allow future clicks to trigger bg listener
      chrome.action.setPopup({ popup: "" });
      // Close the popup windows
      window.close();
    } else {
      throw new Error("Authentication failed");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Authentication failed");
  }
}

export async function sendActiveUrl(token) {
  try {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const currentUrl = tabs[0].url;
    const response = await fetch(`${API_HOST}/api/v1/articles/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ url: currentUrl }),
    });
    return response;
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to send URL");
  }
}

export function checkTokenValidity(exp) {
  const now = Date.now();
  const expTimestamp = new Date(exp).getTime();
  return now < expTimestamp;
}
