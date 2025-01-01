-- Create the database schema

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique user ID
    name TEXT NOT NULL,                          -- Full name of the user
    email TEXT NOT NULL UNIQUE,                  -- Email address (unique)
    username TEXT NOT NULL UNIQUE,               -- Unique username for the user
    profile_picture_url TEXT DEFAULT 'default-profile.jpg', -- URL/path to profile picture
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when user account was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when profile is updated
);

CREATE TABLE IF NOT EXISTS flood_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    status TEXT DEFAULT 'Unverified',
    description TEXT NOT NULL,
    image_url TEXT,
    video_url TEXT,
    location TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP,
    verified_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES users(user_id) ON DELETE SET NULL
);


-- Add an index
CREATE INDEX IF NOT EXISTS idx_report_status ON flood_reports(status);

-- Insert test data
INSERT INTO users (name, email, username, profile_picture_url)
VALUES
    ('Hannah Peterson', 'hannah.111@gmail.com', 'hannah', 'path/to/hannah-profile.jpg'),
    ('John Doe', 'john.doe@gmail.com', 'john', 'path/to/john-profile.jpg');

INSERT INTO flood_reports (user_id, status, description, image_url, video_url, location)
VALUES
    (1, 'Unverified', 'Severe flooding in downtown area. Streets are submerged.', 'path/to/flood-image.jpg', 'path/to/flood-video.mp4', 'Downtown, City'),
    (2, 'Unverified', 'Flooding caused by heavy rain in the suburbs. Several homes affected.', 'path/to/suburb-flood.jpg', 'path/to/suburb-flood-video.mp4', 'Suburbs, City');

-- Verify the inserted data
SELECT * FROM users;
SELECT * FROM flood_reports;
