const API = "http://127.0.0.1:5000";

function login() {
  fetch(`${API}/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      email: email.value,
      password: password.value
    })
  })
  .then(res => res.json())
  .then(data => {
    localStorage.setItem("token", data.access_token);
    window.location = "dashboard.html";
  });
}

function register() {
  fetch(`${API}/register`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name: name.value,
      email: email.value,
      password: password.value
    })
  }).then(() => window.location = "login.html");
}