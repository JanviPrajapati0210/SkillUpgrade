/**
 * Local Knowledge Base
 * Acts as a standalone "database" for skill mapping
 */
const skillDatabase = {
    "data scientist": ["python", "machine learning", "statistics", "sql", "pandas", "visualization"],
    "frontend developer": ["html", "css", "javascript", "react", "tailwind", "git"],
    "backend developer": ["node.js", "express", "postgresql", "api design", "docker", "redis"],
    "fullstack developer": ["react", "node.js", "mongodb", "javascript", "css", "deployment"],
    "ui/ux designer": ["figma", "prototyping", "user research", "wireframing", "adobe xd"],
    "it support": ["networking", "troubleshooting", "active directory", "hardware", "linux"]
};

// Initialize Progress Chart (Global scope for updates)
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
        animation: { duration: 1500 }
    }
});

/**
 * Main Analysis Logic
 */
function analyzeSkills() {
    const jobTitleInput = document.getElementById('jobTitle').value.trim().toLowerCase();
    const userSkillsInput = document.getElementById('userSkills').value.toLowerCase();
    
    // Convert comma-separated string to cleaned array
    const userSkills = userSkillsInput.split(',').map(s => s.trim()).filter(s => s !== "");

    // 1. Check if job title exists in our local map
    if (skillDatabase[jobTitleInput]) {
        const requiredSkills = skillDatabase[jobTitleInput];
        
        // Find missing skills
        const missing = requiredSkills.filter(skill => !userSkills.includes(skill));
        const matchedCount = requiredSkills.length - missing.length;
        
        updateUI(missing, matchedCount, requiredSkills.length);
    } 
    // 2. Fallback: Dynamic analysis if job is unknown
    else {
        handleUnknownJob(userSkills);
    }
}

/**
 * Updates the Visual Dashboard
 */
function updateUI(missing, matched, total) {
    const percent = Math.round((matched / total) * 100);

    // Update Missing Skills Tags
    const container = document.getElementById('missingSkillsContainer');
    if (missing.length > 0) {
        container.innerHTML = missing.map(s => `<span class="skill-tag">${s.toUpperCase()}</span>`).join('');
    } else {
        container.innerHTML = `<p style="color: #4cc9f0;">✨ You have all the core skills for this role!</p>`;
    }

    // Update Chart
    progressChart.data.datasets[0].data = [percent, 100 - percent];
    progressChart.update();
    
    // Update Percentage Label
    document.getElementById('chart-label').innerText = percent + "%";

    // Update Suggested Courses
    const list = document.getElementById('courseList');
    if (missing.length > 0) {
        list.innerHTML = missing.slice(0, 3).map(s => 
            `<li>🚀 <strong>Skillupgrade Path:</strong> ${s.charAt(0).toUpperCase() + s.slice(1)} Mastery</li>`
        ).join('');
    } else {
        list.innerHTML = `<li>🏆 Recommended: Advanced Leadership & Strategy</li>`;
    }
}

/**
 * Fallback for jobs not in the local "database"
 */
function handleUnknownJob(userSkills) {
    // If the job isn't recognized, we simulate a "generic" requirement 
    // or notify the user. Here, we'll suggest common industry gaps.
    const genericGaps = ["System Design", "Cloud Architecture", "Agile Methodology"];
    const filteredGaps = genericGaps.filter(s => !userSkills.includes(s.toLowerCase()));
    
    alert("Title not in local database. Showing general industry standard gaps for high-level roles.");
    updateUI(filteredGaps, userSkills.length, userSkills.length + filteredGaps.length);
}