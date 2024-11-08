CREATE DATABASE IF NOT EXISTS flood_monitor;

USE flood_monitor;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,     -- Unique user ID
    name VARCHAR(255) NOT NULL,                 -- Full name of the user
    email VARCHAR(255) NOT NULL UNIQUE,         -- Email address (unique)
    username VARCHAR(100) NOT NULL UNIQUE,      -- Unique username for the user
    profile_picture_url VARCHAR(255) DEFAULT 'default-profile.jpg', -- URL/path to profile picture
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when user account was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Timestamp for when profile is updated
);

CREATE TABLE IF NOT EXISTS flood_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique report ID
    user_id INT,                               -- Foreign key for the user who submitted the report
    status ENUM('Unverified', 'Verified') DEFAULT 'Unverified', -- Report status (default is 'Unverified')
    description TEXT NOT NULL,                 -- Description of the flood event
    image_url VARCHAR(255),                    -- URL/path to the uploaded image (if any)
    video_url VARCHAR(255),                    -- URL/path to the uploaded video (if any)
    location VARCHAR(255) NOT NULL,            -- The location of the flood event
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the report was submitted
    verified_at TIMESTAMP NULL,                -- Timestamp when the report was verified (if applicable)
    verified_by INT NULL,                      -- ID of the government official who verified the report (foreign key)
    
    -- Foreign key
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE, -- Cascading delete when user is deleted
    FOREIGN KEY (verified_by) REFERENCES users(user_id) ON DELETE SET NULL -- Sets verified_by to NULL when the government official is deleted
);

CREATE INDEX idx_report_status ON flood_reports(status);


SELECT * FROM users;
SELECT * FROM flood_reports;


-- TEST DATA
INSERT INTO users (name, email, username, profile_picture_url) 
VALUES 
    ('Hannah Peterson', 'hannah.111@gmail.com', 'hannah', 'path/to/hannah-profile.jpg'),
    ('John Doe', 'john.doe@gmail.com', 'john', 'path/to/john-profile.jpg');

INSERT INTO flood_reports (user_id, status, description, image_url, video_url, location) 
VALUES 
    (1, 'Unverified', 'Severe flooding in downtown area. Streets are submerged.', 'path/to/flood-image.jpg', 'path/to/flood-video.mp4', 'Downtown, City'),
    (2, 'Unverified', 'Flooding caused by heavy rain in the suburbs. Several homes affected.', 'path/to/suburb-flood.jpg', 'path/to/suburb-flood-video.mp4', 'Suburbs, City');





