from werkzeug.security import generate_password_hash, check_password_hash
import db
def get_user(user_id):
    sql = """
        SELECT id, username 
        FROM users WHERE id = ?
    """
    result = db.query(sql, [user_id])
    return result[0] if result else None



def get_user_posts(user_id):
    sql = """
        SELECT I.id, I.title, U.id user_id, U.username, ROUND(AVG(R.overall_score),2) average_score, COUNT(R.id) review_count
        FROM images I 
        JOIN Users U ON I.user_id = U.id
        LEFT JOIN Reviews R ON R.image_id = I.id
        WHERE I.user_id = ?
        GROUP BY I.id
        ORDER BY I.id DESC
    """
    return db.query(sql, [user_id])

def get_user_review_ratios(user_id):
    sql = """
            SELECT

            (SELECT IFNULL(COUNT(*),0) FROM reviews
             WHERE user_id=?) AS review_count_given,

            (SELECT IFNULL(ROUND(AVG(overall_score),2), 0) FROM reviews
             WHERE user_id=?) AS average_score_given,
            
            (SELECT IFNULL(COUNT(R.id),0) FROM Reviews R 
                JOIN images I ON I.id = R.image_id
                WHERE I.user_id = ?) AS review_count_received,

            (SELECT IFNULL(ROUND(AVG(R.overall_score),2), 0) FROM Reviews R 
                JOIN images I ON I.id = R.image_id
                WHERE I.user_id = ?) AS average_score_received
"""
    return db.query(sql, [user_id, user_id, user_id, user_id])[0]




def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    password_hash = result[0]["password_hash"]
    user_id = result[0]["id"]

    if check_password_hash(password_hash, password):
        return user_id
    return None
