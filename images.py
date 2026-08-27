import db
def add_image(title, description, focal_length, location, user_id, classes):
    sql = """
        INSERT INTO images 
        (title, description, focal_length, geolocation, user_id) 
        VALUES 
        (?, ?, ?, ?, ?)
        """
    db.execute(sql, [title, description, focal_length, location, user_id])

    image_id = db.last_insert_id()
    sql = "INSERT INTO image_classes (image_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [image_id, title, value])


def update_image(image_id, title, description, focal_length, location, user_id, classes):
    sql = """
        UPDATE images 
        SET
        title=?, description=?, focal_length=?, geolocation=?, user_id=? 
        WHERE id = ?
        """
    db.execute(sql, [title, description, focal_length, location, user_id, image_id])
    sql = "DELETE FROM image_classes WHERE image_id = ?"
    db.execute(sql, [image_id])

    sql = "INSERT INTO image_classes (image_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [image_id, title, value])


def remove_image(image_id):
    sql = "DELETE FROM image_classes WHERE image_id = ?"
    db.execute(sql, [image_id])

    sql = "DELETE FROM images WHERE id = ?"
    db.execute(sql, [image_id])
def get_images():
    sql = """
        SELECT id, title FROM images ORDER BY id DESC
    """
    return db.query(sql)

def search_image(query):
    sql = """
    SELECT id, title
    FROM images
    WHERE description LIKE ?
    OR title LIKE ?
    ORDER BY id DESC
    """
    like = "%"+query+"%"
    return db.query(sql, [like, like])

def get_image(image_id):
    sql = """
        SELECT I.id image_id, I.title, I.description, I.focal_length, I.geolocation, U.username, I.user_id 
        FROM images I, users U 
        WHERE I.user_id = U.id
        AND I.id = ?"""
    result = db.query(sql, [image_id])
    return result[0] if result else None

def get_classes(image_id):
    sql = "SELECT title, value FROM image_classes WHERE image_id = ?"
    return db.query(sql, [image_id])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)
    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def add_review(image_id, user_id, score, rationale):
    sql = """INSERT INTO reviews (image_id, user_id, overall_score, rationale)
    VALUES (?, ?, ?, ?)"""
    db.execute(sql, [image_id, user_id, score, rationale])
def get_reviews(image_id):
    sql = """
            SELECT reviews.overall_score score, users.id user_id, users.username, reviews.rationale
            FROM reviews, users
            WHERE reviews.image_id = ? AND reviews.user_id = users.id
            ORDER BY reviews.id DESC  
        """
    return db.query(sql, [image_id])