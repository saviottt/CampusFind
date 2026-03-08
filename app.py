from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from functools import wraps

app = Flask(__name__)
app.secret_key = "campfind_secret_key"

# ================= DATABASE CONFIG =================

DB_HOST = "sql112.infinityfree.com"
DB_USER = "if0_41336411"
DB_PASSWORD = "rcKsHvM0PnL8zdu"
DB_NAME = "if0_41336411_CampFind"

# ===================================================


def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


# ================= LOGIN REQUIRED =================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ================= HOME =================

@app.route("/")
def index():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT p.product_id, p.product_name, p.price, p.image,
               u.name AS seller
        FROM products p
        JOIN users u ON p.seller_id = u.user_id
        ORDER BY p.created_at DESC
    """)

    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", products=products)


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        hashed = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
            (name, email, hashed, role)
        )

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

        if user and (check_password_hash(user["password"], password) or user["password"] == password):

            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]

            return redirect(url_for("index"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")


# ================= ADD PRODUCT =================

@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        product_name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (product_name, description, price, seller_id)
            VALUES (%s,%s,%s,%s)
            """,
            (product_name, description, price, session["user_id"])
        )

        db.commit()

        cursor.close()
        db.close()

        flash("Product added successfully", "success")

        return redirect(url_for("index"))

    return render_template("add_product.html")


# ================= ORDER PRODUCT =================

@app.route("/order/<int:product_id>")
@login_required
def order(product_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO orders (buyer_id, product_id) VALUES (%s,%s)",
        (session["user_id"], product_id)
    )

    db.commit()

    cursor.close()
    db.close()

    flash("Order placed successfully", "success")

    return redirect(url_for("index"))


# ================= MY ORDERS =================

@app.route("/my-orders")
@login_required
def my_orders():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT o.order_id,
               p.product_name,
               u.name AS seller,
               o.status,
               o.order_date
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        JOIN users u ON p.seller_id = u.user_id
        WHERE o.buyer_id=%s
        ORDER BY o.order_date DESC
    """, (session["user_id"],))

    orders = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("orders.html", orders=orders)


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# ================= RUN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)