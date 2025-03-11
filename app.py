import os

import bcrypt
import MySQLdb
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "dt_perpus"

mysql = MySQL(app)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if "loggedin" in session and "role" in session and session["role"] == "admin":
        return render_template("admin_dashboard.html")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_user = request.form["id_perpus"]
        password = request.form["password"].encode("utf-8")

        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "SELECT id_perpus, password, role FROM tbl_mhs WHERE id_perpus = %s",
                (id_user.encode("utf-8"),),
            )

            user = cur.fetchone()
            if user:
                hashedpw = user[1].encode("utf-8")
                if bcrypt.checkpw(password, hashedpw):
                    session["loggedin"] = True
                    session["id_perpus"] = id_user
                    session["role"] = user[2]
                    if session["role"] == "admin":
                        return redirect(url_for("admin_dashboard"))
                    else:
                        return redirect(url_for("dashboard"))
                else:
                    flash("Password salah", "error")
            else:
                flash("ID tidak ditemukan", "error")

        except MySQLdb.Error as e:
            flash(f"Terjadi kesalahan MySQL: {e}", "error")
        except Exception as e:
            flash(f"Terjadi kesalahan Umum: {e}", "error")

        finally:
            cur.close()

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
