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
        document
        .getElementById('jobTitle')
        .value.trim();

    const skillsInput =
        document
        .getElementById('userSkills')
        .value;

    const level =
        document
        .getElementById('difficultyLevel').value;


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

            "Authorization":
                "Bearer " +
                localStorage.getItem("access_token")
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

        saveProgress(
            data.job_domain,
            data.progress
        );

    });

}


/* ------------------ UPDATE UI ------------------ */

function updateUI(
    missing,
    percent,
    roadmap
) {

    /* Missing Skills */

    const container =
        document.getElementById(
            'missingSkillsContainer'
        );


    if (missing.length > 0) {

        container.innerHTML =
            missing
            .map(skill =>
                `<span class="skill-tag">
                    ${skill.toUpperCase()}
                 </span>`
            )
            .join("");

    }
    else {

        container.innerHTML =
            `<p style="color:#4cc9f0;">
            ✨ You already meet all required skills!
            </p>`;
    }


    /* Chart */

    progressChart
        .data
        .datasets[0]
        .data = [
            percent,
            100 - percent
        ];

    progressChart.update();


    document
        .getElementById("chart-label")
        .innerText =
        percent + "%";


    /* Course Roadmap */

    const list =
        document.getElementById(
            "courseList"
        );


    if (missing.length > 0) {

        list.innerHTML =
            Object.keys(roadmap)
            .slice(0, 5)
            .map(skill => {

                const course =
                    roadmap[skill];

                return `
                <li>
                🚀 <b>${skill}</b> →
                <a href="${course.link}"
                   target="_blank">
                   ${course.title}
                </a>
                </li>
                `;

            })
            .join("");

    }
    else {

        list.innerHTML =
            `<li>
            🏆 Recommended:
            Advanced Industry Projects
            </li>`;
    }

}


/* ------------------ SAVE PROGRESS ------------------ */

function saveProgress(
    skill,
    progress
) {

    fetch(`${API}/save-progress`, {

        method: "POST",

        headers: {

            "Content-Type":
                "application/json",

            "Authorization":
                "Bearer " +
                localStorage.getItem(
                    "access_token"
                )
        },

        body: JSON.stringify({

            skill: skill,

            progress: progress
        })

    })

    .then(res => res.json())

    .then(data => {

        console.log(
            "Progress saved:",
            data
        );

    })

    .catch(err => {

        console.error(
            "Save progress failed",
            err
        );

    });

}