async function analyze() {
    const domain = document.getElementById("domain").value;
    const skills = document.getElementById("skills").value.split(",");

    const token = localStorage.getItem("token");

    const response = await fetch("http://127.0.0.1:5000/api/analyze-skills", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            job_domain: domain,
            skills: skills
        })
    });

    const data = await response.json();

    document.getElementById("result").innerHTML =
        "<h3>Missing Skills:</h3>" +
        data.missing_skills.join(", ");
}
