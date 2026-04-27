const BASE_URL = "http://127.0.0.1:8000";

let storedSkills = [];
let storedResumeText = "";

// ----------------------
// SIGNUP
// ----------------------
async function signupUser() {
  const username = document.getElementById("username")?.value.trim();
  const email = document.getElementById("email")?.value.trim();
  const password = document.getElementById("password")?.value.trim();
  const resultBox = document.getElementById("authResult");

  try {
    const response = await fetch(`${BASE_URL}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    resultBox.style.display = "block";
    resultBox.innerHTML = data.message || "Signup completed";

  } catch (error) {
    resultBox.style.display = "block";
    resultBox.innerHTML = "Error connecting to server";
  }
}


// ----------------------
// LOGIN
// ----------------------
async function loginUser() {
  const email = document.getElementById("email")?.value.trim();
  const password = document.getElementById("password")?.value.trim();
  const resultBox = document.getElementById("authResult");

  try {
    const response = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      window.location.href = "/dashboard";
    } else {
      resultBox.style.display = "block";
      resultBox.innerHTML = data.detail || "Login failed";
    }

  } catch (error) {
    resultBox.style.display = "block";
    resultBox.innerHTML = "Server error";
  }
}


// ----------------------
// UPLOAD RESUME
// ----------------------
async function uploadResume() {
  const fileInput = document.getElementById("resumeFile");
  const resultBox = document.getElementById("resumeResult");

  if (!fileInput.files.length) {
    alert("Please select a PDF file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch(`${BASE_URL}/upload-resume`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
      body: formData
    });

    const data = await response.json();

    // ✅ FIXED KEY
    storedSkills = data.resume_skills || [];
    storedResumeText = data.extracted_text || "";

    console.log("Resume Skills:", storedSkills);

    resultBox.style.display = "block";

    if (storedSkills.length === 0) {
      resultBox.innerHTML = "⚠️ No skills detected. Try another resume.";
    } else {
      resultBox.innerHTML = `
        <strong>Extracted Skills:</strong><br><br>
        ${storedSkills.map(skill => `<span class='badge'>${skill}</span>`).join("")}
      `;
    }

  } catch (error) {
    resultBox.style.display = "block";
    resultBox.innerHTML = "Error uploading resume";
  }
}


// ----------------------
// ANALYZE JOB
// ----------------------
async function analyzeJob() {
  const jd = document.getElementById("jobDescription").value.trim();

  if (!jd) {
    alert("Please enter a job description");
    return;
  }

  if (storedSkills.length === 0) {
    alert("Please upload resume first");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/analyze-job`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({
        resume_skills: storedSkills,
        job_description: jd
      })
    });

    const data = await response.json();

    console.log("Analysis Result:", data);

    localStorage.setItem("finalResult", JSON.stringify(data));
    window.location.href = "/result";

  } catch (error) {
    alert("Error analyzing job");
  }
}


// ----------------------
// RESULT PAGE RENDER
// ----------------------
window.onload = function () {
  const resultBox = document.getElementById("finalResult");

  if (!resultBox) return;

  const data = JSON.parse(localStorage.getItem("finalResult") || "{}");

  resultBox.innerHTML = `
    <strong>ATS Score:</strong> ${data.ats_score || 0}%<br><br>

    <strong>Insight:</strong> ${data.insight || "No insight available"}<br><br>

    <strong>Matched Skills:</strong><br>
    ${(data.matched_skills || []).map(skill => `<span class='badge green'>${skill}</span>`).join("")}
    
    <br><br>

    <strong>Missing Skills:</strong><br>
    ${(data.missing_skills || []).map(skill => `<span class='badge red'>${skill}</span>`).join("")}
    
    <br><br>

    <strong>Suggestions:</strong><br>
    ${(data.suggestions || []).map(item => `• ${item}<br>`).join("")}
  `;
};