document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.prediction-container form');
  const resultsSection = document.getElementById('results');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Optionally get month and year values
    const month = document.getElementById('month').value;
    const year = document.getElementById('year').value;

    // Optional: show temporary output
    const resultsOutput = document.getElementById('results-output');
    resultsOutput.innerHTML = `<p>Predicting ARI Risk for ${month}/${year}...</p>`;

    // Scroll to results section
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  });
});
