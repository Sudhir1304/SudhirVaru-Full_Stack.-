-- Create database
CREATE DATABASE crickscore;
USE crickscore;

-- Create matches table
CREATE TABLE matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    current_score INT DEFAULT 0,
    wickets INT DEFAULT 0,
    current_over INT DEFAULT 0,
    current_ball INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create balls table
CREATE TABLE balls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    over_number INT,
    ball_number INT,
    runs INT,
    is_out BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id)
);

-- Insert initial match
INSERT INTO matches (current_score, wickets, current_over, current_ball) 
VALUES (0, 0, 0, 0);