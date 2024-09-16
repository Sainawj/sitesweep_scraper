document.addEventListener('DOMContentLoaded', function() {
    const scrapeForm = document.getElementById('scrapeForm');
    const resultTitle = document.getElementById('resultTitle');
    const resultDescription = document.getElementById('resultDescription');
    const resultEmails = document.getElementById('resultEmails');
    const resultPhones = document.getElementById('resultPhones');
    const resultAddresses = document.getElementById('resultAddresses');
    const historyTableBody = document.querySelector('#historyTable tbody');

    // Handle scraping form submission
    scrapeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(scrapeForm);
        fetch('/api/scrape', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Scraping successful!") {
                // Populate the result section
                resultTitle.textContent = data.data.title;
                resultDescription.textContent = data.data.description;
                resultEmails.textContent = data.data.emails.join(', ') || "No emails found";
                resultPhones.textContent = data.data.phones.join(', ') || "No phone numbers found";
                resultAddresses.textContent = data.data.addresses.join(', ') || "No addresses found";
            } else {
                alert("Scraping failed: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // Fetch and populate scraping history
    function fetchHistory() {
        fetch('/api/history')
            .then(response => response.json())
            .then(data => {
                // Clear the table body
                historyTableBody.innerHTML = '';
                // Populate table rows with history records
                data.slice(0, 10).forEach(record => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${record.id}</td>
                        <td>${record.url}</td>
                        <td>${new Date(record.date).toLocaleString()}</td>
                        <td>${record.status}</td>
                    `;
                    historyTableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Error fetching history:", error);
            });
    }

    // Fetch history on page load
    fetchHistory();
});
