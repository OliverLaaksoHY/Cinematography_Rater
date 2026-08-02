import db
def add_item(title, description, focal_length, location, user_id):
    sql = """
        INSERT INTO items 
        (title, description, focal_length, geolocation, user_id) 
        VALUES 
        (?, ?, ?, ?, ?)
        """
    db.execute(sql, [title, description, focal_length, location, user_id])

def update_item(item_id, title, description, focal_length, location, user_id):
    sql = """
        UPDATE items 
        SET
        title=?, description=?, focal_length=?, geolocation=?, user_id=? 
        WHERE id = ?
        """
    db.execute(sql, [title, description, focal_length, location, user_id, item_id])


def get_items():
    sql = """
        SELECT id, title FROM items ORDER BY id DESC
    """
    return db.query(sql)


def get_item(item_id):
    sql = """
        SELECT I.id item_id, I.title, I.description, I.focal_length, I.geolocation, U.username, I.user_id 
        FROM items I, users U 
        WHERE I.user_id = U.id
        AND U.id = ?"""
    result = db.query(sql, [item_id])[0]
    return result