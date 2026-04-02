/* ------------------ CHART INIT ------------------ */

const ctx = document
    .getElementById('progressChart')
    .getContext('2d');

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


/* ------------------ ANALYZE SKILLS ------------------ */

function analyzeSkills() {

    const jobDomain =
        document.getElementById('jobTitle').value.trim();

    const skillsInput =
        document.getElementById('userSkills').value;

    const level =
        document.getElementById('difficultyLevel').value;


    const userSkills = skillsInput
        .split(',')
        .map(s => s.trim())
        .filter(s => s !== "");


    if (!jobDomain) {
        alert("Please enter a job domain");
        return;
    }


    const token = localStorage.getItem("access_token");

    // 🔥 FIRST: ANALYZE SKILLS
    fetch(`${API}/analyze-skills`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            job_domain: jobDomain,
            skills: userSkills,
            level: level
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
            data.progress,
            data.roadmap
        );

        saveProgress(jobDomain, data.progress);

        // 🔥 SECOND: GET ML RECOMMENDATIONS
        return fetch(`${API}/recommend-courses`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                skills: userSkills.join(",")
            })
        });

    })
    .then(res => res.json())
    .then(recData => {

        if (recData.error) return;

        updateRecommendations(recData);

    })
    .catch(err => {
        console.error("Error:", err);
    });

}


/* ------------------ UPDATE MAIN UI ------------------ */

function updateUI(missing, percent, roadmap) {

    /* Missing Skills */

    const container =
        document.getElementById('missingSkillsContainer');

    if (missing.length > 0) {

        container.innerHTML =
            missing.map(skill =>
                `<span class="skill-tag">
                    ${skill.toUpperCase()}
                 </span>`
            ).join("");

    } else {

        container.innerHTML =
            `<p style="color:#4cc9f0;">
            ✨ You already meet all required skills!
            </p>`;
    }


    /* Chart */

    progressChart.data.datasets[0].data = [
        percent,
        100 - percent
    ];

    progressChart.update();

    document.getElementById("chart-label").innerText =
        percent + "%";


    /* 🚀 ROADMAP */

    const list =
        document.getElementById("courseList");

    if (missing.length > 0) {

        list.innerHTML =
            Object.keys(roadmap)
            .slice(0, 5)
            .map(skill => {

                const course = roadmap[skill];

                return `
                <li>
                🚀 <b>${skill}</b> →
                <a href="${course.link}" target="_blank">
                   ${course.title}
                </a>
                </li>
                `;

            }).join("");

    } else {

        list.innerHTML =
            `<li>🏆 You are fully ready! Try advanced projects 🚀</li>`;
    }
}


/* ------------------ UPDATE ML RECOMMENDATIONS ------------------ */
function updateRecommendations(data) {

    const existingDiv =
        document.getElementById("existingCourses");

    existingDiv.innerHTML = "";

    data.existing_skill_courses?.forEach(item => {

        let html = `
        <div class="skill-card">

            <div class="skill-header">
                <span class="dot"></span>
                ${item.skill}
            </div>
        `;
item.recommended_courses.forEach(course => {
    html += `
        <div class="course-card"
             onclick="window.open('${course.link}', '_blank')">

            <h4>${course.course_name}</h4>

            <p>
                Upgrade your ${item.skill} skill with this course
            </p>

        </div>
    `;
});

       html += `</div></div>`;

        existingDiv.innerHTML += html;
    });

}

/* ------------------ SAVE PROGRESS ------------------ */

function saveProgress(skill, progress) {

    fetch(`${API}/save-progress`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization":
                "Bearer " +
                localStorage.getItem("access_token")
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


/* ------------------ LOGOUT ------------------ */

function logout() {

    localStorage.removeItem("access_token");

    alert("Logged out successfully");

    window.location.href = "login.html";
}