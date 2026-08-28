import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response
import db
import images
import users
import secrets
import re
app = Flask(__name__)
app.secret_key = str(secrets.token_hex(16))


def try_fetch_image(image_id: int):
    image = images.get_image(image_id)
    if not image:
        abort(404)
    return image

def try_fetch_image_with_rights(image_id: int):
    image = images.get_image(image_id)
    if not image:
        print("Aborting here")
        abort(404)
    
    if not session.get("user_id") or image["user_id"] != session["user_id"]:
        print("Aborting here2")
        abort(403)
    return image

def require_login():
    if not session.get("user_id"):
        print("aborting fro require_login")
        abort(403)

def check_csrf():
    token = request.form["csrf_token"]
    if not token or token != session["csrf_token"]:
        abort(403)
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(403)
    images = users.get_user_posts(user_id)
    ratio = users.get_user_review_ratios(user_id)
    print(ratio["review_count_given"])
    return render_template("show_user.html", user=user, images=images, ratio=ratio)


@app.route("/")
def index():
    all_images = images.get_images()
    return render_template("index.html", images=all_images)

@app.route("/find_image")
def find_image():
    query = request.args.get("query")
    if query:
        results = images.search_image(query)
    else:
        query = ""
        results = []
    
    return render_template("find_image.html", query=query, results=results)


@app.route("/imagefile/<int:image_id>")
def show_imagefile(image_id):
    image = images.get_image(image_id)
    imagefile = image["imagefile"]
    if not imagefile:
        abort(404)

    response = make_response(bytes(imagefile))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = try_fetch_image(image_id)
    classes = images.get_classes(image_id)
    reviews = images.get_reviews(image_id)
    print(reviews)
    return render_template("show_image.html", image=image, classes=classes, reviews=reviews)

@app.route("/edit_image/<int:image_id>")
def edit_image(image_id):
    require_login()
    image = try_fetch_image_with_rights(image_id)
    all_classes = images.get_all_classes()
    classes = {}
    for entry in classes:
        classes[entry] = []

    for entry in images.get_classes(image_id):
        classes[entry["title"]] = entry["value"] 
    return render_template("edit_image.html", image=image, classes=classes, all_classes = all_classes)

@app.route("/update_image", methods=["POST"])
def update_image():
    check_csrf()
    image_id = request.form["image_id"]
    try_fetch_image_with_rights(image_id)

    title = request.form["title"]
    if len(title) > 50 or not title:
        abort(403)
    description = request.form["description"]
    if len(description) > 500 or not description:
        abort(403)
    focal_length = request.form["focal_length"]
    if not re.search("^[1-9][0-9]{0,3}$", focal_length):
        abort(403)
    location = request.form["location"]
    if not location:
        abort(403)

    user_id = session["user_id"]

    all_classes = images.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
                
            classes.append((class_title, class_value))


    try:
        images.update_image(image_id, title, description, focal_length, location, user_id, classes)
    except sqlite3.IntegrityError:
        return "Already exists"

    return redirect("/image/"+str(image_id))

@app.route("/remove_image/<int:image_id>", methods = ["GET", "POST"])
def remove_image(image_id):
    image = try_fetch_image_with_rights(image_id)
    
    if request.method == "GET":
        return render_template("remove_image.html", image=image)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            images.remove_image(image_id)
            return redirect("/")
        else:
            return redirect("/image/"+str(image_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add_image")
def add_image():
    require_login()
    classes = images.get_all_classes()
    return render_template("add_image.html", classes = classes)



@app.route("/create_review", methods=["POST"])
def create_review():
    check_csrf()
    require_login()
    score = request.form["score"]
    if not re.search("^[0-5]$", score):
        print("Wrong score")
        abort(403)
    rationale = request.form["rationale"]
    if not rationale or len(rationale) > 300:
        abort(403) 
    image_id = request.form["image_id"]
    image = try_fetch_image(image_id)

    images.add_review(image_id, session["user_id"], score, rationale)
    return redirect("/image/"+str(image_id))

@app.route("/create_image", methods=["POST"])
def create_image():
    check_csrf()
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50: 
        abort(403)
    
    description = request.form["description"]
    if not description or len(description) > 500 :
        abort(403)

    focal_length = request.form["focal_length"]
    if not re.search("^[1-9][0-9]{0,3}$", focal_length):
        abort(403)
    
    location = request.form["location"]
    if not location:
        abort(403)

    file = request.files["image"]
    if not file.filename.lower().endswith(".jpg"):
        return "VIRHE: Wrong file format"

    image = file.read()
    if len(image) > 10 * 1000 * 1024:
        return "VIRHE: Image file too large "

    
    classes = []
    user_id = session["user_id"]
    
    all_classes = images.get_all_classes()

    
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
    
            classes.append((class_title, class_value))


    
    try:
        images.add_image(title, image, description, focal_length, location, user_id, classes)
    except sqlite3.IntegrityError:
        return "Already exists"

    return redirect("/")

   
@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    
    return "Tunnus luotu"
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)
        if user_id:    
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
