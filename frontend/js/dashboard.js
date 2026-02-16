fetch("http://127.0.0.1:5000/analyze-skills", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("token")}`
  },
  body: JSON.stringify({})   // send user data if required later
})
.then(res => res.json())
.then(data => {

  const currentDiv = document.getElementById("currentSkills");
  const missingDiv = document.getElementById("missingSkills");

  let completed = data.current_skills.length;
  let total = completed + data.missing_skills.length;

  // ✅ CURRENT SKILLS
  data.current_skills.forEach(skill => {
    currentDiv.innerHTML += `
      <div class="skill-card">✅ ${skill}</div>
    `;

    // Save 100% progress for acquired skills
    saveProgress(skill, 100);
  });

  // ❌ MISSING SKILLS
  data.missing_skills.forEach(skill => {
    missingDiv.innerHTML += `
      <div class="skill-card">
        ❌ ${skill}<br>
        <a href="https://www.coursera.org/search?query=${skill}" target="_blank">
          Find Course
        </a>
      </div>
    `;

    // Save 0% progress for missing skills
    saveProgress(skill, 0);
  });

  // 📊 OVERALL PROGRESS
  let progress = Math.round((completed / total) * 100);
  document.getElementById("progressBar").value = progress;
  document.getElementById("progressText").innerText = progress + "%";
});

function saveProgress(skill, progress) {
  fetch("http://127.0.0.1:5000/save-progress", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({
      skill: skill,
      progress: progress
    })
  });
}