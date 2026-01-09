async function analyze() {
  const jobFile = document.getElementById("jobFile").files[0];
  const resumeFiles = document.getElementById("resumeFiles").files;

  if (!jobFile || resumeFiles.length === 0) {
    alert("Please upload job file and resumes");
    return;
  }

  const formData = new FormData();
  formData.append("job_file", jobFile);

  for (let i = 0; i < resumeFiles.length; i++) {
    formData.append("resumes", resumeFiles[i]);
  }

  document.getElementById("output").innerHTML = "Processing...";

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    renderResults(data.ranked_resumes);

  } catch (error) {
    console.error(error);
    document.getElementById("output").innerHTML = "Error processing files";
  }
}

function renderResults(results) {
  const output = document.getElementById("output");
  output.innerHTML = "";

  results.forEach((res, index) => {
    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
      <h3>Rank ${index + 1} – ${res.resume_id}</h3>
      <p class="score">Match Score: ${res.match_score}%</p>
      <p><strong>Matched Skills:</strong> ${res.matched_skills.join(", ")}</p>
      <p><strong>Missing Skills:</strong> ${res.missing_skills.join(", ")}</p>
      <div class="llm">
        <strong>LLM Explanation:</strong><br/>
        ${res.llm_explanation}
      </div>
    `;

    output.appendChild(div);
  });
}
