import sqlite3
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session, make_response
import db
import images
import users
import secrets
import re
import markupsafe


app = Flask(__name__)
app.secret_key = str(secrets.token_hex(16))

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


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
        print("require_login")
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
    require_login()
    image_id = request.form["image_id"]
    try_fetch_image_with_rights(image_id)

    title = request.form["title"].strip("/n")
    if len(title) > 50 or not title:
        flash("Error: Title must be between 1 and 50 letters")
        return redirect("/update_image")

    description = request.form["description"]
    if len(description) > 500 or not description:
        flash("Error: Description must be between 1 and 500 letters")
        return redirect("/update_image")
    focal_length = request.form["focal_length"]
    if not re.search("^[1-9][0-9]{0,3}$", focal_length):
        flash("Error: Focal length must be between 1mm and 999 mm")
        return redirect("/update_image")
    
    location = request.form["location"].strip("/n")
    if not location:
        flash("Error: A location is required")
        return redirect("/update_image")

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
    image_id = request.form["image_id"]
    
    if not re.search("^[0-5]$", score):
        flash("Error: Score must be either 0, 1, 2, 3, 4 or 5")
        return redirect("/image/"+str(image_id))
    rationale = request.form["rationale"]
    if len(rationale) > 300:
        flash("Error: Rationale has a max length of 300")
        return redirect("/image/"+str(image_id))
    try_fetch_image(image_id)

    images.add_review(image_id, session["user_id"], score, rationale)
    return redirect("/image/"+str(image_id))

@app.route("/create_image", methods=["POST"])
def create_image():
    check_csrf()
    require_login()

    title = request.form["title"].strip("/n")
    if len(title) > 50 or not title:
        flash("Error: Title must be between 1 and 50 letters")
        return redirect("/add_image")

    description = request.form["description"]
    if len(description) > 500 or not description:
        flash("Error: Description must be between 1 and 500 letters")
        return redirect("/update_image")
    focal_length = request.form["focal_length"]
    if not re.search("^[1-9][0-9]{0,3}$", focal_length):
        flash("Error: Focal length must be between 1mm and 999 mm")
        return redirect("/add_image")
    
    location = request.form["location"].strip("/n")
    if not location:
        flash("Error: A location is required")
        return redirect("/add_image")
        
    file = request.files["image"]
    if not file:
        flash("Error: No image given")
        return redirect("/add_image")
       
    
    if not (file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".png")):
        flash("Error: Wrong file format (jpg or png)")
        return redirect("/add_image")

    image = file.read()
    if len(image) > 10 * 1000 * 1000:
        flash("Error: Image file size too large (above 10 MB)")
        return redirect("/add_image")
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
        flash("Error: Passwords do not match")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("Error: Username taken")
        return redirect("/register")
    flash("account successfully created")
    return redirect("/login")
    

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
            flash("Wrong username or password")
            return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
