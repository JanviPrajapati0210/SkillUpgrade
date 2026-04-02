const API = "http://127.0.0.1:5000/api";


/* ================= TOKEN ================= */

function getToken() {
    return localStorage.getItem("access_token");
}


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

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            alert("Login successful");

            window.location.href = "dashboard.html";

        } else {

            alert(data.error || "Login failed");
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

            window.location.href = "login.html";

        } else {

            alert(data.error || "Registration failed");
        }
    })

    .catch(err => {
        console.error(err);
        alert("Server error");
    });
}


/* ================= ANALYZE SKILLS ================= */

function analyzeSkillsAPI(data) {

    return fetch(`${API}/analyze-skills`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify(data)
    }).then(res => res.json());
}


/* ================= ML RECOMMENDATION ================= */

function recommendCoursesAPI(skills) {

    return fetch(`${API}/recommend-courses`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({
            skills: skills
        })
    }).then(res => res.json());
}


/* ================= SAVE PROGRESS ================= */

function saveProgressAPI(skill, progress) {

    return fetch(`${API}/save-progress`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({
            skill: skill,
            progress: progress
        })
    }).then(res => res.json());
}


/* ================= LOGOUT ================= */

function logout() {

    fetch(`${API}/logout`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + getToken()
        }
    })
    .then(() => {

        localStorage.removeItem("access_token");

        alert("Logged out successfully");

        window.location.href = "login.html";
    })
    .catch(() => {

        localStorage.removeItem("access_token");

        window.location.href = "login.html";
    });
}