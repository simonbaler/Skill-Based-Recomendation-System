document.getElementById('details-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const nameInput = document.getElementById('name-input').value;
    const skillsInput = document.getElementById('skills-input').value;
    const domainInput = document.getElementById('domain-input').value;
    const gpaInput = document.getElementById('gpa-input').value;
    const resultsDiv = document.getElementById('results');

    // Show a loading message
    resultsDiv.innerHTML = '<p>Loading recommendations...</p>';

    const userData = {
        name: nameInput,
        skills: skillsInput,
        domain: domainInput,
        gpa: gpaInput
    };

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        resultsDiv.innerHTML = '<h2>Recommendations</h2>'; // Clear previous results and add title
        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach(rec => {
                resultsDiv.innerHTML += `
                    <div class="recommendation-item">
                        <h4>${rec.title}</h4>
                        <p>Match Score: <strong>${rec.score}%</strong></p>
                    </div>
                `;
            });
        } else {
            resultsDiv.innerHTML += '<p>No recommendations found for the given details.</p>';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        resultsDiv.innerHTML = '<p>Sorry, something went wrong while fetching recommendations. Please check the console for more details.</p>';
    });
});

