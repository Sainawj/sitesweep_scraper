CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scraping_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    data TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255),
    description TEXT,
    emails TEXT,
    phones TEXT,
    addresses TEXT,
    status VARCHAR(50) DEFAULT 'Completed',
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


