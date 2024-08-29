import { login } from "./lib.js";

document.addEventListener("DOMContentLoaded", function () {
  const authForm = document.getElementById("kn-authForm");
  const frame = document.getElementById("kn-frame");
  authForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(authForm);
    login(formData);
  });
});
