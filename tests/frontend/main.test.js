// main.test.js

const fetchMock = require('jest-fetch-mock');
fetchMock.enableMocks();

beforeEach(() => {
    fetch.resetMocks();
});

test('should fetch scraping history and update the DOM', async () => {
    document.body.innerHTML = `
        <table>
            <tbody></tbody>
        </table>
    `;

    // Mock API response for the history fetch
    fetch.mockResponseOnce(JSON.stringify([
        { id: 1, url: 'https://example.com', date: '2024-09-12', status: 'Completed' }
    ]));

    const response = await fetch('/api/history');
    const data = await response.json();

    const historyTable = document.querySelector('tbody');
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.url}</td>
            <td>${item.date}</td>
            <td>${item.status}</td>
        `;
        historyTable.appendChild(row);
    });

    expect(historyTable.innerHTML).toContain('https://example.com');
    expect(historyTable.querySelectorAll('tr').length).toBe(1);
});
