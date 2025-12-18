from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date, timedelta

app = Flask(__name__)
DB_NAME = "gym.db"


# ---------- DB CONNECTION ----------
def get_db():
    conn = sqlite3.connect("gym.db")
    conn.row_factory = sqlite3.Row  # ✅ THIS IS THE FIX
    return conn


# ---------- INIT DB ----------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        duration INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memberships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        plan_id INTEGER,
        start_date TEXT,
        end_date TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------- HOME ----------
@app.route("/")
def home():
    return redirect("/members")


# ---------- MEMBERS LIST ----------
@app.route("/members")
def members():
    conn = get_db()
    today = date.today().isoformat()

    rows = conn.execute("""
    SELECT 
        m.id,
        m.name,
        m.phone,
        p.name,
        ms.end_date
    FROM members m
    LEFT JOIN memberships ms ON m.id = ms.member_id
    LEFT JOIN plans p ON ms.plan_id = p.id
    ORDER BY m.id DESC
    """).fetchall()

    conn.close()

    members = []
    for r in rows:
        is_active = r[4] and r[4] >= today
        members.append({
            "id": r[0],
            "name": r[1],
            "phone": r[2],
            "plan": r[3],
            "end_date": r[4],
            "active": is_active
        })

    return render_template("members.html", members=members, today=today)


# ---------- ADD MEMBER ----------
@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO members (name, phone) VALUES (?, ?)",
            (request.form["name"], request.form["phone"])
        )
        conn.commit()
        conn.close()
        return redirect("/members")

    return render_template("add_member.html")


# ---------- DELETE MEMBER (SAFE) ----------
@app.route("/members/delete/<int:member_id>")
def delete_member(member_id):
    conn = get_db()
    today = date.today().isoformat()

    active = conn.execute("""
        SELECT 1 FROM memberships
        WHERE member_id = ?
        AND end_date >= ?
    """, (member_id, today)).fetchone()

    if active:
        conn.close()
        return "❌ Cannot delete member with active membership"

    conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
    return redirect("/members")


# ---------- PLANS ----------
@app.route("/plans", methods=["GET", "POST"])
def plans():
    conn = get_db()

    if request.method == "POST":
        conn.execute(
            "INSERT INTO plans (name, duration) VALUES (?, ?)",
            (request.form["name"], request.form["duration"])
        )
        conn.commit()

    plans = conn.execute("SELECT * FROM plans").fetchall()
    conn.close()
    return render_template("plans.html", plans=plans)


# ---------- ASSIGN / RENEW ----------
@app.route("/assign/<int:member_id>", methods=["GET", "POST"])
def assign(member_id):
    conn = get_db()

    member = conn.execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,)
    ).fetchone()

    plans = conn.execute(
        "SELECT * FROM plans"
    ).fetchall()

    if request.method == "POST":
        plan_id = request.form["plan_id"]

        row = conn.execute(
            "SELECT duration_days FROM plans WHERE id = ?",
            (plan_id,)
        ).fetchone()

        duration_days = row["duration_days"]  # ✅ NOW THIS WORKS

        start_date = date.today()
        end_date = start_date + timedelta(days=duration_days)

        conn.execute(
            """
            INSERT INTO memberships (member_id, plan_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
            """,
            (member_id, plan_id, start_date, end_date)
        )

        conn.commit()
        conn.close()
        return redirect("/members")

    conn.close()
    return render_template(
        "assign.html",
        member=member,
        plans=plans
    )



# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
