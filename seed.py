import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM reviews")
db.execute("DELETE FROM images")
db.execute("DELETE FROM users")

user_count = 1000
image_count = 10**5
review_count = 10**6
# USERS
for i in range(1, user_count + 1):
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ["user" + str(i), "pswd"]
    )

# IMAGES
with open("small_image_test.png", "rb") as file:
    image_data = file.read()

for i in range(1, image_count + 1):
    user_id = random.randint(1, user_count)

    db.execute(
        """INSERT INTO images
           (title, image, description, focal_length, geolocation, user_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            "image" + str(i), image_data, "description" + str(i), random.randint(1, 999), "location" + str(i), user_id]
    )

# REVIEWS
for i in range(1, review_count + 1):
    user_id = random.randint(1, user_count)
    image_id = random.randint(1, image_count)

    db.execute(
        """INSERT INTO reviews
           (image_id, user_id, overall_score, rationale)
           VALUES (?, ?, ?, ?)""",
        [image_id, user_id, random.randint(0, 5), "review" + str(i)]
    )

db.commit()
db.close()

