DROP DATABASE IF EXISTS diarydb;
CREATE DATABASE diarydb;
USE diarydb;

CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    created_date DATE
);

CREATE TABLE notes(
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(50),
    content TEXT,
    created_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);