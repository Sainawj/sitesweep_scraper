CREATE TABLE scraping_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    data TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255),
    description TEXT,
    emails TEXT,
    phones TEXT,
    addresses TEXT;
    status VARCHAR(50) DEFAULT 'Completed'
);
