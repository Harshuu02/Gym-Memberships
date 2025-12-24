from datetime import date

REMINDER_DAYS = 7  # configurable

def get_expiring_members(conn):
    today = date.today().isoformat()
    upcoming = []

    rows = conn.execute("""
        SELECT m.name, m.phone, ms.end_date
        FROM memberships ms
        JOIN members m ON ms.member_id = m.id
        WHERE ms.end_date >= ?
    """, (today,)).fetchall()

    for r in rows:
        days_left = (date.fromisoformat(r["end_date"]) - date.today()).days
        if 0 <= days_left <= REMINDER_DAYS:
            upcoming.append({
                "name": r["name"],
                "phone": r["phone"],
                "days_left": days_left
            })

    return upcoming
