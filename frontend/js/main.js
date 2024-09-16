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

        // Make a request to the scraping API
        fetch('/api/scrape', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Scraping successful!") {
                // Populate the result section
                resultTitle.textContent = data.data.title || "No title found";
                resultDescription.textContent = data.data.description || "No description found";
                resultEmails.textContent = data.data.emails.length ? data.data.emails.join(', ') : "No emails found";
                resultPhones.textContent = data.data.phones.length ? data.data.phones.join(', ') : "No phone numbers found";
                resultAddresses.textContent = data.data.addresses.length ? data.data.addresses.join(', ') : "No addresses found";

                // Optionally, fetch the history again to update the table
                fetchHistory();
            } else {
                alert("Scraping failed: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred during scraping. Please try again.");
        });
    });

    // Function to open popup with scraped data
    function openPopup(data) {
        const popup = document.getElementById('popup');
        const scrapedDataDiv = document.getElementById('scrapedData');
        scrapedDataDiv.innerHTML = `
            <p><strong>Title:</strong> ${data.title || "No title found"}</p>
            <p><strong>Description:</strong> ${data.description || "No description found"}</p>
            <p><strong>Emails:</strong> ${data.emails.length ? data.emails.join(', ') : "No emails found"}</p>
            <p><strong>Phones:</strong> ${data.phones.length ? data.phones.join(', ') : "No phone numbers found"}</p>
            <p><strong>Addresses:</strong> ${data.addresses.length ? data.addresses.join(', ') : "No addresses found"}</p>
        `;
        popup.style.display = 'block';
    }

    // Close popup when clicking close button
    document.getElementById('closePopup').addEventListener('click', function() {
        document.getElementById('popup').style.display = 'none';
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
                        <td><button onclick="fetchScrapedData(${record.id})">Details</button></td>
                    `;
                    historyTableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Error fetching history:", error);
            });
    }

    // Function to fetch scraped data by ID
    window.fetchScrapedData = function(id) {
        fetch(`/api/scraped_data/${id}`)
            .then(response => response.json())
            .then(data => openPopup(data))
            .catch(error => console.error('Error fetching scraped data:', error));
    };

    // Fetch history on page load
    fetchHistory();
});
