CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    image BLOB,
    description TEXT,
    focal_length INTEGER,
    geolocation TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images,
    user_id INTEGER REFERENCES users,
    overall_score INTEGER,
    rationale TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE image_classes (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images,
    title TEXT,
    value TEXT 
);