import sqlite3

DB_NAME = "threat_dashboard.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        threat TEXT,
        abuse_score INTEGER,
        search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_search(ip, threat, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO search_history(ip, threat, abuse_score)
    VALUES (?, ?, ?)
    """, (ip, threat, score))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ip, threat, abuse_score, search_time, id
    FROM search_history
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def clear_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM search_history")

    conn.commit()
    conn.close()


def delete_history_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM search_history WHERE id = ?",
        (item_id,)
    )

    conn.commit()
    conn.close()


# ==========================
# Dashboard Statistics
# ==========================

def get_statistics():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM search_history")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM search_history WHERE threat='Safe'")
    safe = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM search_history WHERE threat='Suspicious'")
    suspicious = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM search_history WHERE threat='Malicious'")
    malicious = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "safe": safe,
        "suspicious": suspicious,
        "malicious": malicious
    }