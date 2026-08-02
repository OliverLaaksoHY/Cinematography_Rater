import db
def add_item(title, description, focal_length, location, user_id):
    sql = """
        INSERT INTO items 
        (title, description, focal_length, geolocation, user_id) 
        VALUES 
        (?, ?, ?, ?, ?)
        """
    db.execute(sql, [title, description, focal_length, location, user_id])

def get_items():
    sql = """
        SELECT id, title FROM items ORDER BY id DESC
    """
    return db.query(sql)


def get_item(item_id):
    sql = """
        SELECT I.title, I.description, I.focal_length, I.geolocation, U.username, user_id 
        FROM items I, users U 
        WHERE I.user_id = U.id
        AND U.id = ?"""
    result = db.query(sql, [item_id])[0]
    return result