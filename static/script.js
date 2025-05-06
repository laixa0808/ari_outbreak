document.addEventListener("DOMContentLoaded", function () {
  const resultsSection = document.getElementById("results");
  if (resultsSection && resultsSection.innerText.trim().length > 0) {
      resultsSection.scrollIntoView({ behavior: "smooth" });
  }
});
