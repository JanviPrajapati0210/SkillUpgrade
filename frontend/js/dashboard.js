/* ================================
   SkillUpgrade – Dashboard Logic
   ================================ */

/* ---------- API BASE URL ---------- */
const API_BASE = "http://127.0.0.1:5000";

/* ---------- ELEMENT REFERENCES ---------- */
const domainSelect = document.getElementById("jobDomain");
const titleSelect = document.getElementById("jobTitle");
const skillsInput = document.getElementById("skills");
const resultBox = document.getElementById("result");

/* ---------- THEME TOGGLE ---------- */
function toggleTheme() {
  document.body.classList.toggle("dark");

  // Save preference
  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark") ? "dark" : "light"
  );
}

/* ---------- LOAD SAVED THEME ---------- */
(function loadTheme() {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
  }
})();

/* ---------- LOAD JOB DOMAINS ---------- */
async function loadDomains() {
  try {
    const res = await fetch(`${API_BASE}/domains`);
    const data = await res.json();

    domainSelect.innerHTML = `<option value="">Select Job Domain</option>`;

    data.domains.forEach(domain => {
      const option = document.createElement("option");
      option.value = domain;
      option.textContent = domain;
      domainSelect.appendChild(option);
    });

  } catch (error) {
    alert("Failed to load job domains");
  }
}

/* ---------- LOAD JOB TITLES ---------- */
async function loadTitles() {
  const domain = domainSelect.value;
  titleSelect.innerHTML = `<option value="">Loading...</option>`;

  if (!domain) return;

  try {
    const res = await fetch(`${API_BASE}/titles/${domain}`);
    const data = await res.json();

    titleSelect.innerHTML = `<option value="">Select Job Title</option>`;

    data.titles.forEach(title => {
      const option = document.createElement("option");
      option.value = title;
      option.textContent = title;
      titleSelect.appendChild(option);
    });

  } catch (error) {
    alert("Failed to load job titles");
  }
}

/* ---------- ANALYZE SKILLS ---------- */
async function analyzeSkills() {
  const domain = domainSelect.value;
  const title = titleSelect.value;
  const userSkills = skillsInput.value
    .split(",")
    .map(skill => skill.trim())
    .filter(skill => skill !== "");

  if (!domain || !title || userSkills.length === 0) {
    alert("Please fill all fields");
    return;
  }

  const payload = {
    job_domain: domain,
    job_title: title,
    skills: userSkills
  };

  resultBox.innerHTML = "🔍 Analyzing your skills...";

  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    renderResult(data);

  } catch (error) {
    resultBox.innerHTML = "❌ Server error. Please try again.";
  }
}

/* ---------- RENDER RESULT ---------- */
function renderResult(data) {
  resultBox.innerHTML = "";

  const missing = data.missing_skills;
  const roadmap = data.roadmap;

  if (missing.length === 0) {
    resultBox.innerHTML = `
      <h3>🎉 Congratulations!</h3>
      <p>You already meet the required skills for this role.</p>
    `;
    return;
  }

  let html = `<h3>📌 Missing Skills</h3><ul>`;

  missing.forEach(skill => {
    html += `<li><strong>${skill}</strong> – ${roadmap[skill]}</li>`;
  });

  html += `</ul>`;
  resultBox.innerHTML = html;
}

/* ---------- LOGOUT ---------- */
function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

/* ---------- INITIAL LOAD ---------- */
loadDomains();
