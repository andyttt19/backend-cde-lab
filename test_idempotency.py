import sqlite3

DB_PATH = "cde_lab.db"
conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
    SELECT id, transaction_ref, idempotency_key
    FROM [transaction]
    WHERE idempotency_key IS NOT NULL
""")

rows = cursor.fetchall()
print("Giao dịch có khóa:", rows)

try:
    cursor.execute("""
        INSERT INTO [transaction]
            (status, amount, transaction_ref, created_at, idempotency_key)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "pending",
        100,
        "test-duplicate-ref",
        "2026-10-14 00:00:00",
        rows[0][2]
    ))

    conn.commit()
    print("LỖI: Database đã chấp nhận khóa trùng!")

except sqlite3.IntegrityError as error:
    conn.rollback()
    print("Đã chặn khóa trùng:", error)

finally:
    conn.close()