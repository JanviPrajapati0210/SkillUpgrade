function toggleTheme() {
    const body = document.body;
    body.classList.toggle("dark");
    body.classList.toggle("light");

    localStorage.setItem("theme", body.className);
}

window.onload = function () {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.body.className = savedTheme;
}
