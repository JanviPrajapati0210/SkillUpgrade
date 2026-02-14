const API = "http://127.0.0.1:5000/api";

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await response.json();

    if(data.access_token){
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    } else {
        alert(data.message);
    }
}
