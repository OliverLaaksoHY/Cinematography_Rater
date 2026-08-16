import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import items
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
        abort(404)
    
    if not session.get("user_id") or item["user_id"] != session["user_id"]:
        abort(403)
    return item

def require_login():
    if not session.get("user_id"):
        abort(403)


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
    return render_template("show_item.html", item=item)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = try_fetch_item_with_rights(item_id)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    item = try_fetch_item_with_rights(item_id)

    title = request.form["title"]
    if len(title) > 50 or not title:
        abort(403)
    
    description = request.form["description"]
    if len(description) > 500 or not description:
        abort(403)

    focal_length = request.form["focal_length"]
    if not re.search("^[1-9][0-9]{0, 3}$", focal_length):
        abort(403)
    
    location = request.form["location"]
    if not location:
        abort(403)
    user_id = session["user_id"]
    try:
        items.update_item(item_id, title, description, focal_length, location, user_id)
    except sqlite3.IntegrityError:
        return "Already exists"

    return redirect("/item/"+str(item_id))

@app.route("/remove_item/<int:item_id>", methods = ["GET", "POST"])
def remove_item(item_id):
    item = try_fetch_item_with_rights(item_id)
    
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
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
    return render_template("add_cinema.html")

@app.route("/create_item", methods=["POST"])
def create_item():
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
    
    user_id = session["user_id"]
    
    try:
        items.add_item(title, description, focal_length, location, user_id)
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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
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
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        
        result = db.query(sql, [username])[0]
        password_hash = result["password_hash"]
        user_id = result["id"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
