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
            const url = document.getElementById('scrapeUrl').value;
            try {
                const response = await fetch('/api/scrape', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `url=${encodeURIComponent(url)}`
                });
                const result = await response.json();
                if (response.ok) {
                    alert('Scraping successful!');
                    // Handle result.data to update the UI as needed
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Fetch and Display History
    async function loadHistory() {
        try {
            const response = await fetch('/api/history');
            const history = await response.json();
            const historyTable = document.getElementById('historyTable');
            if (historyTable) {
                history.forEach(record => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${record.id}</td>
                        <td>${record.url}</td>
                        <td>${record.date}</td>
                        <td>${record.status}</td>
                        <td><button class="editButton" data-id="${record.id}">Edit</button></td>
                        <td><button class="deleteButton" data-id="${record.id}">Delete</button></td>
                    `;
                    historyTable.appendChild(row);
                });

                // Attach event listeners for edit and delete buttons
                document.querySelectorAll('.editButton').forEach(button => {
                    button.addEventListener('click', function() {
                        const id = this.dataset.id;
                        // Handle edit logic
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
            console.error('Error:', error);
        }
    }

    if (document.getElementById('historyTable')) {
        loadHistory();
    }

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
                console.error('Error:', error);
            }
        });
    }
});
