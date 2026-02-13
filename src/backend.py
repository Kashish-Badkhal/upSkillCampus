import psycopg2
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

# --- REPORT COMPLIANCE: Load Key from Environment Variable  ---
def get_key():
    """Loads the master encryption key from the environment variable."""
    key = os.getenv('MASTER_ENCRYPTION_KEY')
    if not key:
        # Fallback for safety, though report implies env var is mandatory
        raise ValueError("MASTER_ENCRYPTION_KEY not found in .env file!")
    return key.encode() if isinstance(key, str) else key

def encrypt(message):
    f = Fernet(get_key())
    return f.encrypt(message.encode()).decode()

def decrypt(token):
    f = Fernet(get_key())
    return f.decrypt(token.encode()).decode()

# --- Database Utils ---
def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

def init_db():
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id SERIAL PRIMARY KEY,
                website VARCHAR(100) NOT NULL,
                username VARCHAR(100) NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()

def add_password(website, username, password):
    encrypted_pw = encrypt(password)
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)",
            (website, username, encrypted_pw)
        )
        conn.commit()
        conn.close()
        return True
    return False

def get_passwords(search_query=""):
    conn = get_connection()
    results = []
    if conn:
        cur = conn.cursor()
        if search_query:
            query = "SELECT id, website, username, password FROM passwords WHERE website ILIKE %s OR username ILIKE %s"
            cur.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        else:
            cur.execute("SELECT id, website, username, password FROM passwords")
            
        rows = cur.fetchall()
        for row in rows:
            row_id, site, user, enc_pw = row
            try:
                dec_pw = decrypt(enc_pw)
                results.append((row_id, site, user, dec_pw))
            except Exception:
                results.append((row_id, site, user, "Error: Decryption Failed"))
        conn.close()
    return results

# --- REPORT COMPLIANCE: Update Functionality  ---
def update_password(pw_id, new_site, new_user, new_pass):
    encrypted_pw = encrypt(new_pass)
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE passwords SET website=%s, username=%s, password=%s WHERE id=%s",
            (new_site, new_user, encrypted_pw, pw_id)
        )
        conn.commit()
        conn.close()
        return True
    return False

def delete_password(password_id):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM passwords WHERE id = %s", (password_id,))
        conn.commit()
        conn.close()
        return True
    return False