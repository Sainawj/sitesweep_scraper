// Example: Fetch scraping history when the history page is loaded
document.addEventListener('DOMContentLoaded', async function() {
    if (window.location.pathname.includes('history.html')) {
        try {
            const response = await fetch('/api/history');
            const history = await response.json();

            const historyTable = document.querySelector('tbody');
            history.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.url}</td>
                    <td>${item.date}</td>
                    <td>${item.status}</td>
                `;
                historyTable.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching history:', error);
        }
    }
});
