const API = "http://127.0.0.1:5000/api";


/* ================= LOGIN ================= */

function login() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;


    fetch(`${API}/login`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email,
            password: password
        })

    })

    .then(res => res.json())

    .then(data => {

        if (data.access_token) {

            // save token
            localStorage.setItem(
                "access_token",
                data.access_token
            );

            alert("Login successful");

            window.location.href =
                "dashboard.html";

        }

        else {

            alert(
                data.error || "Login failed"
            );

        }

    })

    .catch(err => {

        console.error(err);

        alert("Server error");

    });

}



/* ================= REGISTER ================= */

function register() {

    const name =
        document.getElementById("name").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;


    fetch(`${API}/register`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name,
            email: email,
            password: password

        })

    })

    .then(res => res.json())

    .then(data => {

        if (data.message) {

            alert("Registration successful");

            window.location.href =
                "login.html";

        }

        else {

            alert(
                data.error ||
                "Registration failed"
            );

        }

    })

    .catch(err => {

        console.error(err);

        alert("Server error");

    });

}



/* ================= LOGOUT ================= */

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    window.location.href =
        "login.html";

}



/* ================= GET TOKEN ================= */

function getToken() {

    return localStorage.getItem(
        "access_token"
    );

}