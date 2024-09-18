document.addEventListener('DOMContentLoaded', function() {
    // Handle Login Form Submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                if (response.ok) {
                    window.location.href = result.redirect || '/';
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Handle Logout
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', async function() {
            try {
                const response = await fetch('/logout');
                if (response.ok) {
                    window.location.href = '/';
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Handle Scraping Form Submission
    const scrapeForm = document.getElementById('scrapeForm');
    if (scrapeForm) {
        scrapeForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(scrapeForm);
            try {
                const response = await fetch('/api/scrape', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                if (response.ok) {
                    // Populate the result section
                    document.getElementById('resultTitle').textContent = result.data.title || "No title found";
                    document.getElementById('resultDescription').textContent = result.data.description || "No description found";
                    document.getElementById('resultEmails').textContent = result.data.emails.length ? result.data.emails.join(', ') : "No emails found";
                    document.getElementById('resultPhones').textContent = result.data.phones.length ? result.data.phones.join(', ') : "No phone numbers found";
                    document.getElementById('resultAddresses').textContent = result.data.addresses.length ? result.data.addresses.join(', ') : "No addresses found";
                    alert('Scraping successful!');
                    fetchHistory();  // Optionally fetch the history again to update the table
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Fetch and Display History
    async function fetchHistory() {
        try {
            const response = await fetch('/api/history');
            const history = await response.json();
            const historyTableBody = document.querySelector('#historyTable tbody');
            if (historyTableBody) {
                historyTableBody.innerHTML = '';
                history.slice(0, 10).forEach(record => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${record.id}</td>
                        <td>${record.url}</td>
                        <td>${new Date(record.date).toLocaleString()}</td>
                        <td>${record.status}</td>
                        <td><a href="#" onclick="fetchScrapedData(${record.id}); return false;">View Details</a></td>
                        <td><button class="editButton" data-id="${record.id}">Edit</button></td>
                        <td><button class="deleteButton" data-id="${record.id}">Delete</button></td>
                    `;
                    historyTableBody.appendChild(row);
                });

                // Debugging line to check if edit buttons are selected
                console.log('Edit buttons:', document.querySelectorAll('.editButton'));

                // Attach event listeners for edit and delete buttons
                document.querySelectorAll('.editButton').forEach(button => {
                    button.addEventListener('click', async function() {
                        const id = this.dataset.id;
                        console.log('Edit button clicked, ID:', id); // Debugging line
                        try {
                            const response = await fetch(`/api/record/${id}`);
                            const data = await response.json();
                            if (response.ok) {
                                // Populate the edit form with existing data
                                document.getElementById('editRecordId').value = data.id;
                                document.getElementById('editUrl').value = data.url;
                                document.getElementById('editDate').value = new Date(data.date).toLocaleDateString();
                                document.getElementById('editStatus').value = data.status;
                                document.getElementById('editModal').style.display = 'block';  // Show the edit modal
                            } else {
                                alert(data.message);
                            }
                        } catch (error) {
                            console.error('Error fetching record data:', error);
                        }
                    });
                });

                document.querySelectorAll('.deleteButton').forEach(button => {
                    button.addEventListener('click', async function() {
                        const id = this.dataset.id;
                        try {
                            const response = await fetch(`/api/delete_record/${id}`, {
                                method: 'DELETE'
                            });
                            const result = await response.json();
                            if (response.ok) {
                                alert('Record deleted successfully!');
                                this.closest('tr').remove();
                            } else {
                                alert(result.message);
                            }
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    });
                });
            }
        } catch (error) {
            console.error('Error fetching history:', error);
        }
    }

    // Handle Edit Form Submission
    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(editForm);
            try {
                const response = await fetch('/api/update_record', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                if (response.ok) {
                    alert('Record updated successfully!');
                    document.getElementById('editModal').style.display = 'none';  // Hide the edit modal
                    fetchHistory();  // Refresh the history table
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error updating record:', error);
            }
        });
    }

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

    // Function to fetch scraped data by ID
    window.fetchScrapedData = function(id) {
        fetch(`/api/scraped_data/${id}`)
            .then(response => response.json())
            .then(data => openPopup(data))
            .catch(error => console.error('Error fetching scraped data:', error));
    };

    // Handle Export CSV Button
    const exportCsvButton = document.getElementById('exportCsvButton');
    if (exportCsvButton) {
        exportCsvButton.addEventListener('click', async function() {
            try {
                const response = await fetch('/api/export_csv');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'scraping_history.csv';
                document.body.appendChild(a);
                a.click();
                a.remove();
            } catch (error) {
                console.error('Error exporting CSV:', error);
            }
        });
    }

    // Initial fetch of scraping history
    fetchHistory();
});
