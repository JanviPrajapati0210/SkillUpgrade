const API = "http://127.0.0.1:5000/api";

/* ------------------ CHART INIT ------------------ */

const ctx = document.getElementById('progressChart').getContext('2d');
let progressChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Matched', 'Missing'],
        datasets: [{
            data: [0, 100],
            backgroundColor: ['#f72585', '#e2e8f0'],
            hoverOffset: 4,
            borderWidth: 0
        }]
    },
    options: {
        cutout: '85%',
        plugins: { legend: { display: false } },
        animation: { duration: 1200 }
    }
});

/* ------------------ ANALYZE SKILLS (CSV) ------------------ */

function analyzeSkills() {
    const jobDomain = document.getElementById('jobTitle').value.trim();
    const skillsInput = document.getElementById('userSkills').value;

    const userSkills = skillsInput
        .split(',')
        .map(s => s.trim())
        .filter(s => s !== "");

    if (!jobDomain) {
        alert("Please enter a job domain");
        return;
    }

    fetch(`${API}/analyze-skills`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token")
        },
        body: JSON.stringify({
            job_domain: jobDomain,
            skills: userSkills
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        updateUI(
            data.missing_skills,
            data.known_skills,
            data.total_required_skills,
            data.progress_percentage,
            data.roadmap
        );
    
      saveProgress(data.job_domain, data.progress_percentage);
    });
}

/* ------------------ UPDATE DASHBOARD UI ------------------ */

function updateUI(missing, matched, total, percent, roadmap) {

    /* Missing Skills */
    const container = document.getElementById('missingSkillsContainer');

    if (missing.length > 0) {
        container.innerHTML = missing
            .map(skill => `<span class="skill-tag">${skill.toUpperCase()}</span>`)
            .join("");
    } else {
        container.innerHTML =
            `<p style="color:#4cc9f0;">✨ You already meet all required skills!</p>`;
    }

    /* Update Chart */
    progressChart.data.datasets[0].data = [percent, 100 - percent];
    progressChart.update();

    /* Percentage Label */
    document.getElementById("chart-label").innerText = percent + "%";

    /* Suggested Learning Roadmap */
    const list = document.getElementById("courseList");

    if (missing.length > 0) {
        list.innerHTML = Object.keys(roadmap)
            .slice(0, 3)
            .map(skill =>
                `<li>🚀 <strong>SkillUpgrade Path:</strong> ${roadmap[skill]}</li>`
            )
            .join("");
    } else {
        list.innerHTML =
            `<li>🏆 Recommended: Advanced Industry Projects & Leadership Skills</li>`;
    }
}

function saveProgress(skill, progress) {
    fetch(`${API}/save-progress`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token")
        },
        body: JSON.stringify({
            skill: skill,
            progress: progress
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Progress saved:", data);
    })
    .catch(err => {
        console.error("Save progress failed", err);
    });
}
