<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitesweep</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <script src="{{ url_for('static', filename='js/main.js') }}" defer></script>
    <style>
        /* Inline CSS for the popup */
        #popup {
            display: none; /* Initially hidden */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            color: #fff;
            z-index: 1000;
        }

        #popupContent {
            margin: 15% auto;
            padding: 20px;
            background: #333;
            border-radius: 10px;
            width: 80%;
            max-width: 600px;
        }

        #closePopup {
            float: right;
            cursor: pointer;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <h1>Sitesweep: Web Scraping Tool</h1>

    <!-- Form to input the URL -->
    <form id="scrapeForm">
        <label for="url">Enter URL to Scrape:</label>
        <input type="text" id="url" name="url" placeholder="https://example.com" required>
        <button type="submit">Scrape</button>
    </form>

    <h2>Scraped Data</h2>
    <div id="scrapedResults">
        <p><strong>Title:</strong> <span id="resultTitle">N/A</span></p>
        <p><strong>Description:</strong> <span id="resultDescription">N/A</span></p>
        <p><strong>Emails:</strong> <span id="resultEmails">N/A</span></p>
        <p><strong>Phones:</strong> <span id="resultPhones">N/A</span></p>
        <p><strong>Addresses:</strong> <span id="resultAddresses">N/A</span></p>
    </div>

    <h2>Scraping History</h2>
    <table id="historyTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>URL</th>
                <th>Date</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
            <!-- Dynamic rows go here -->
        </tbody>
    </table>

    <!-- Popup Modal -->
    <div id="popup">
        <div id="popupContent">
            <span id="closePopup">&times;</span>
            <h2>Scraped Data</h2>
            <div id="scrapedData">Loading...</div>
        </div>
    </div>
</body>
</html>
