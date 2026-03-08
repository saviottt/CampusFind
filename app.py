from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pymysql
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "campusfind_secret_key"

# ================= DATABASE CONFIG =================

DB_HOST = "mysql-1bf966e3-donsavio1one-abfd.a.aivencloud.com"
DB_USER = "avnadmin"
DB_PASSWORD = "AVNS_nRzIR6lr_GryFlZkKuw"
DB_NAME = "online_store"
DB_PORT = 27223

# ================= FILE UPLOAD =================

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


# ================= DATABASE CONNECTION =================

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        ssl={"ssl": {}},
        cursorclass=pymysql.cursors.DictCursor
    )


# ================= HELPER FUNCTIONS =================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ================= HOME =================

@app.route("/")
def index():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT items.*, users.name AS owner_name
        FROM items
        JOIN users ON items.user_id = users.id
        ORDER BY items.created_at DESC
        LIMIT 10
    """)

    items = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", items=items)


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        student_id = request.form["student_id"]
        department = request.form["department"]

        hashed_password = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users (name,email,password,student_id,department)
            VALUES (%s,%s,%s,%s,%s)
        """, (name, email, hashed_password, student_id, department))

        db.commit()

        cursor.close()
        db.close()

        flash("Registration successful", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("index"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# ================= REPORT LOST / FOUND =================

@app.route("/report/<item_type>", methods=["GET", "POST"])
@login_required
def report_item(item_type):

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        description = request.form["description"]
        location = request.form["location"]
        date_occurred = request.form["date_occurred"]
        contact_info = request.form["contact_info"]

        image_path = None

        if "image" in request.files:

            file = request.files["image"]

            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

                file.save(
                    os.path.join(app.config["UPLOAD_FOLDER"], filename)
                )

                image_path = filename

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO items
            (user_id,type,title,category,description,location,date_occurred,contact_info,image_path)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            item_type,
            title,
            category,
            description,
            location,
            date_occurred,
            contact_info,
            image_path
        ))

        db.commit()

        cursor.close()
        db.close()

        flash("Item reported successfully", "success")

        return redirect(url_for("index"))

    return render_template("report.html", item_type=item_type)


# ================= ITEM DETAIL =================

@app.route("/item/<int:item_id>")
def item_detail(item_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT items.*, users.name AS owner_name
        FROM items
        JOIN users ON items.user_id = users.id
        WHERE items.id=%s
    """, (item_id,))

    item = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("item_detail.html", item=item)


# ================= PROFILE =================

@app.route("/profile")
@login_required
def profile():

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM items WHERE user_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )

    my_items = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("profile.html", my_items=my_items)


# ================= RUN =================

if __name__ == "__main__":

    os.makedirs(os.path.join("static", "uploads"), exist_ok=True)

    app.run(host="0.0.0.0", port=10000)
