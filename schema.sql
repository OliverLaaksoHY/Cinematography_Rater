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


CREATE UNIQUE INDEX idx_users_id
ON users(id);

CREATE UNIQUE INDEX idx_users_username
ON users(username);

CREATE UNIQUE INDEX idx_images_id
ON images(id);

CREATE UNIQUE INDEX idx_images_title
ON images(title);

CREATE UNIQUE INDEX idx_reviews_id
ON reviews(id);

CREATE UNIQUE INDEX idx_classes_id
ON classes(id);

CREATE UNIQUE INDEX idx_image_classes_id
ON image_classes(id);

CREATE INDEX idx_images_user_id
ON images(user_id);

CREATE INDEX idx_reviews_image_id
ON reviews(image_id);

CREATE INDEX idx_reviews_user_id
ON reviews(user_id);

CREATE INDEX idx_image_classes_image_id
ON image_classes(image_id);