import db
def add_item(title, description, focal_length, location, user_id):
    sql = """
        INSERT INTO items 
        (title, description, focal_length, geolocation, user_id) 
        VALUES 
        (?, ?, ?, ?, ?)
        """
    db.execute(sql, [title, description, focal_length, location, user_id])
    