import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import items
import users
import secrets
import re
app = Flask(__name__)
app.secret_key = str(secrets.token_hex(16))


def try_fetch_item(item_id: int):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return item

def try_fetch_item_with_rights(item_id: int):
    item = items.get_item(item_id)
    if not item:
        print("Aborting here")
        abort(404)
    
    if not session.get("user_id") or item["user_id"] != session["user_id"]:
        print("Aborting here2")
        abort(403)
    return item

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
    items = users.get_user_posts(user_id)
    
    return render_template("show_user.html", user=user, items=items)


@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", message="Tervetuloa!", items=all_items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.search_item(query)
    else:
        query = ""
        results = []
    
    return render_template("find_item.html", query=query, results=results)



@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = try_fetch_item(item_id)
    classes = items.get_classes(item_id)
    reviews = items.get_reviews(item_id)
    print(reviews)
    return render_template("show_item.html", item=item, classes=classes, reviews=reviews)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = try_fetch_item_with_rights(item_id)
    all_classes = items.get_all_classes()
    classes = {}
    for entry in classes:
        classes[entry] = []

    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"] 
    return render_template("edit_item.html", item=item, classes=classes, all_classes = all_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    check_csrf()
    item_id = request.form["item_id"]
    try_fetch_item_with_rights(item_id)

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

    all_classes = items.get_all_classes()
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
        items.update_item(item_id, title, description, focal_length, location, user_id, classes)
    except sqlite3.IntegrityError:
        return "Already exists"

    return redirect("/item/"+str(item_id))

@app.route("/remove_item/<int:item_id>", methods = ["GET", "POST"])
def remove_item(item_id):
    item = try_fetch_item_with_rights(item_id)
    
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/"+str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add_cinema")
def add_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("add_cinema.html", classes = classes)



@app.route("/create_review", methods=["POST"])
def create_review():
    check_csrf()
    require_login()
    score = request.form["score"]
    if not re.search("^[1-5]$", score):
        print("Wrong score")
        abort(403)
    rationale = request.form["rationale"]
    if not rationale or len(rationale) > 300:
        abort(403) 
    item_id = request.form["item_id"]
    item = try_fetch_item(item_id)

    items.add_review(item_id, session["user_id"], score, rationale)
    return redirect("/item/"+str(item_id))

@app.route("/create_item", methods=["POST"])
def create_item():
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
    
    classes = []
    user_id = session["user_id"]
    
    all_classes = items.get_all_classes()

    
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
        items.add_item(title, description, focal_length, location, user_id, classes)
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
