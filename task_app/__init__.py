from flask import Blueprint, render_template, request, redirect
import sqlite3
import os

task_app = Blueprint(
    "task_app",
    __name__,
    template_folder="templates"
)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "tasks.db"
)


def get_db():
    return sqlite3.connect(DB_PATH)


@task_app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@task_app.route("/add", methods=["POST"])
def add():
    titre = request.form["titre"]
    description = request.form["description"]
    date = request.form["date"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (titre, description, date_echeance)
        VALUES (?, ?, ?)
    """, (titre, description, date))

    conn.commit()
    conn.close()

    return redirect("/new")


@task_app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/new")


@task_app.route("/done/<int:id>")
def done(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET terminee = 1
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/new")


