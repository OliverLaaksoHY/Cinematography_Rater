import db
def add_image(title, image, description, focal_length, location, user_id, classes):
    sql = """
        INSERT INTO images 
        (title, image, description, focal_length, geolocation, user_id) 
        VALUES 
        (?, ?, ?, ?, ?, ?)
        """
    db.execute(sql, [title, image, description, focal_length, location, user_id])

    image_id = db.last_insert_id()
    sql = "INSERT INTO image_classes (image_id, title, value) VALUES (?, ?, ?)"
    for class_title, value in classes:
        db.execute(sql, [image_id, class_title, value])


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
    for class_title, value in classes:
        db.execute(sql, [image_id, class_title, value])


def remove_image(image_id):
    sql = "DELETE FROM image_classes WHERE image_id = ?"
    db.execute(sql, [image_id])

    sql = "DELETE FROM reviews WHERE image_id = ?"
    db.execute(sql, [image_id])

    sql = "DELETE FROM images WHERE id = ?"
    db.execute(sql, [image_id])
def get_images(page, page_size):
    sql = """
        SELECT I.id, I.title, U.id user_id, U.username, ROUND(AVG(R.overall_score),2) average_score, COUNT(R.id) review_count
        FROM images I 
        JOIN Users U ON I.user_id = U.id
        LEFT JOIN Reviews R ON R.image_id = I.id
        GROUP BY I.id
        ORDER BY I.id DESC
        LIMIT ? OFFSET ?
    """
    return db.query(sql, [page_size, (page-1)*page_size])

def get_image_count():
    sql = """
        SELECT COUNT(id)
        FROM images
    """
    result = db.query(sql)
    return result[0][0]

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
        SELECT I.id image_id, I.Image imagefile, I.title, I.description, I.focal_length, I.geolocation, U.username, I.user_id,
        ROUND(AVG(R.overall_score),2) average_score,
        COUNT(R.id) review_count
        FROM images I
        LEFT JOIN users U on I.user_id = U.id
        LEFT JOIN reviews R ON I.id = R.image_id 
        WHERE I.id = ?"""
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
