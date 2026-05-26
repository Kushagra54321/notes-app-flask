from flask import Flask, render_template, request, redirect, session
import time 
import mysql.connector
time.sleep(10)

# NEW IMPORTS
from dotenv import load_dotenv
import os

# LOAD .env FILE
load_dotenv()

app = Flask(__name__)

# SECRET KEY FROM .env
app.secret_key = os.getenv("SECRET_KEY")


# ================= DATABASE CONNECTION =================

db = mysql.connector.connect(

    host=os.getenv("DB_HOST"),

    user=os.getenv("DB_USER"),

    password=os.getenv("DB_PASSWORD"),

    database=os.getenv("DB_NAME")

)

cursor = db.cursor()


# ================= HOME PAGE =================

@app.route("/")
def home():

    return render_template("home.html")


# ================= SIGNUP =================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"

        val = (username, password)

        cursor.execute(sql, val)

        db.commit()

        return redirect("/login")

    return render_template("signup.html")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        sql = "SELECT * FROM users WHERE username=%s AND password=%s"

        val = (username, password)

        cursor.execute(sql, val)

        user = cursor.fetchone()

        if user:

            session["user_id"] = user[0]

            return redirect("/notes")

        else:

            return "Invalid Username or Password"

    return render_template("login.html")


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ================= ADD NOTES =================

@app.route("/notes", methods=["GET", "POST"])
def notes():

    # LOGIN CHECK
    if "user_id" not in session:

        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]

        content = request.form["content"]

        sql = """
        INSERT INTO notes (title, content, user_id)
        VALUES (%s, %s, %s)
        """

        val = (title, content, session["user_id"])

        cursor.execute(sql, val)

        db.commit()

    return render_template("index.html")


# ================= YOUR NOTES =================

@app.route("/your-notes")
def your_notes():

    if "user_id" not in session:

        return redirect("/login")

    sql = "SELECT * FROM notes WHERE user_id=%s"

    val = (session["user_id"],)

    cursor.execute(sql, val)

    all_notes = cursor.fetchall()

    return render_template("your_notes.html", notes=all_notes)


# ================= DELETE NOTE =================

@app.route("/delete/<int:id>")
def delete_note(id):

    if "user_id" not in session:

        return redirect("/login")

    sql = "DELETE FROM notes WHERE id=%s"

    val = (id,)

    cursor.execute(sql, val)

    db.commit()

    return redirect("/your-notes")


# ================= EDIT NOTE =================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_note(id):

    if "user_id" not in session:

        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]

        content = request.form["content"]

        sql = """
        UPDATE notes
        SET title=%s, content=%s
        WHERE id=%s
        """

        val = (title, content, id)

        cursor.execute(sql, val)

        db.commit()

        return redirect("/your-notes")

    sql = "SELECT * FROM notes WHERE id=%s"

    val = (id,)

    cursor.execute(sql, val)

    note = cursor.fetchone()

    return render_template("edit_note.html", note=note)


# ================= RUN APP =================
print("New Version Running 😎")
app.run(host="0.0.0.0", port=5000)