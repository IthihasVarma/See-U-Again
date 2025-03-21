document.getElementById('start-button').addEventListener('click', function() {
    document.getElementById('search-form').style.display = 'block';
});

document.getElementById('person-search').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const apiKey = 'YOUR_API_KEY'; // Replace with actual API key if needed

    fetch('/search', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Accept': 'application/json'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data and display results
        document.getElementById('results').style.display = 'block';
        document.getElementById('result-files').innerHTML = JSON.stringify(data.results); // Display results
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('return-home').addEventListener('click', function() {
    document.getElementById('results').style.display = 'none';
    document.getElementById('search-form').style.display = 'none';
});
