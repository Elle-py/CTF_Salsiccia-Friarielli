from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

def init_db():
    # Connessione al database SQLite
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Creazione della tabella se non esiste
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        dashboard_file TEXT NOT NULL,
        secure_login INTEGER DEFAULT 0
    )
    ''')

    # Inserimento degli utenti (3 vulnerabili e uno sicuro)
    users = [
        (1, 'HINT', 'HINT', 'HINT.html', 0),
        (2, 'Oznerol', 'Oznerol','Oznerol.html', 0),
        (3, 'Annavoigairam', 'Annavoigairam', 'Annavoigairam.html', 0),
        (4, 'secure_user', 'SuperSecurePass!', 'secure_user.html', 1),
    ]
    
    # Salva i cambiamenti
    c.executemany("INSERT OR IGNORE INTO users (id, username, password, dashboard_file, secure_login) VALUES (?, ?, ?, ?, ?)", users)
    conn.commit()
    conn.close()

# Percorso sicuro per i file accessibili
BASE_DIR = os.path.join(os.getcwd(), "files")

# Crea directory e file per la demo
os.makedirs(BASE_DIR, exist_ok=True)
with open(os.path.join(BASE_DIR, "example.txt"), "w") as f:
    f.write("Questo è un file demo. Non contiene la flag.")

# Percorso del file protetto
FLAG_PATH = os.path.join(os.getcwd(), "flag.txt")
if not os.path.exists(FLAG_PATH):
    with open(FLAG_PATH, "w") as f:
        f.write("CTF{example_flag}")

# Funzione di login
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Connessione al database per verificare le credenziali
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return redirect(url_for('user_dashboard', username=username))  # Se le credenziali sono corrette, reindirizza al dashboard dell'utente
        else:
            return render_template("index.html", error="Credenziali errate!")
    
    return render_template("index.html")

# Dashboard dell'utente
@app.route("/dashboard/<username>")
def user_dashboard(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Recupera il file HTML associato
    c.execute("SELECT dashboard_file FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user:
        dashboard_file = user[0]
        return render_template(dashboard_file, username=username)
    else:
        return "Utente non trovato."

@app.route("/read", methods=["GET", "POST"])
def read_file():
    if request.method == "POST":
        filename = request.form.get("file")
        if not filename:
            return render_template("read.html", error="Specifica un file!")

        # Verifica del percorso del file
        filepath = os.path.join(BASE_DIR, filename)
        filepath = os.path.join("secrets", filename)
        try:
            if not filepath.startswith(BASE_DIR):  # Protezione contro Directory Traversal
                return render_template("read.html", error="Accesso negato!")

            # Leggi il contenuto del file e visualizzalo nella pagina
            with open(filepath, "r") as f:
                content = f.read()
            return render_template("read.html", content=content)
        except FileNotFoundError:
            return render_template("read.html", error="File non trovato!")
    return render_template("read.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
    

