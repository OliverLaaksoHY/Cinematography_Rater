# PYLINT RAPORT
Pylint gives the following rapport from the app:
```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:6:0: E0401: Unable to import 'flask' (import-error)
app.py:7:0: E0401: Unable to import 'flask' (import-error)
app.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:82:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:107:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:115:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:128:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:176:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:176:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:189:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:193:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:201:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:220:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:220:0: R0911: Too many return statements (9/6) (too-many-return-statements)
app.py:279:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:297:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:297:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:315:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:2:0: E0401: Unable to import 'flask' (import-error)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module images
images.py:1:0: C0114: Missing module docstring (missing-module-docstring)
images.py:2:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:2:0: R0913: Too many arguments (7/5) (too-many-arguments)
images.py:13:8: R1704: Redefining argument with the local name 'title' (redefined-argument-from-local)
images.py:17:0: R0913: Too many arguments (7/5) (too-many-arguments)
images.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:99:0: C0116: Missing function or method docstring (missing-function-docstring)
images.py:104:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:10:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:11:0: C0103: Constant name "image_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:12:0: C0103: Constant name "review_count" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:1:0: E0401: Unable to import 'werkzeug.security' (import-error)
users.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:48:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
```
## Let's go through the raport and justify, why certain pylint-notices have not been fixed in the application:

### Docstring-notices, similar to:

users.py:48:0: C0116: Missing function or method docstring (missing-function-docstring)

A conscious decision regarding the development of this application was made against the use of docstring-comments.

### Import-notices
The pylint raport gives similar noices regarding the import commands:

app.py:6:0: E0401: Unable to import 'flask' (import-error)
app.py:7:0: E0401: Unable to import 'flask' (import-error)

These notices do not matter, becauase the import-commands work in the application itself.

### Missing return statement:
The raport has the similar notices to the following notice regarding missing return statement:
app.py:176:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)

These notices regard a situation, where a function is handling methods "GET" and "POST" but not other methods. For example the notice above is regarding this function.
```python
@app.route("/remove_image/<int:image_id>", methods = ["GET", "POST"])
def remove_image(image_id):
    require_login()
    image = try_fetch_image_with_rights(image_id)
    if request.method == "GET":
        return render_template("remove_image.html", image=image)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            images.remove_image(image_id)
            return redirect("/")
        return redirect("/image/"+str(image_id))
```
The decorator of the function demands that the method has to be either "GET" or "POST". Thus there is no risk of the funciton not returning a value.

### Constant name

The raport has the similar notices like the following notiec regarding constant name: 

seed.py:10:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)

The developer of application is of the opinion that in the situations of these constant name notices, the lower cased versions suit the readability / aesthetics of the code better.

### Too many return statements
The raport has the similar notices to the following notice regarding return statements:

app.py:220:0: R0911: Too many return statements (9/6) (too-many-return-statements)

In the opinion of the developer these cases of having multiple returns are an intentional way to keep the code clean and readable. Introducing dataclasses or nesting functions to alleviate function parameter load would not have any merit to its investment in the opinion of the developer. 

### Dangerous default value
The raport has the following notices regarding default value:

db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)

For example the first notice is regarding to the following function: 
``
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
``
Here the parameters default value [] is an empty list. Here the problem could be, that the same default value list object is divided between all calls of the function and if one particular called list were to have its contents altered, this change would affect other calls as well. In practice in this case it doesn't matter, however, because the code does not alter these list objects.
