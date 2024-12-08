from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
import os
import sqlite3
import sys

app = Flask(__name__)

#disabilitazione del buffering per visualizzare messaggi di [DEBUG]
sys.stdout.reconfigure(line_buffering=True)

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
        dashboard_file TEXT NOT NULL
    )
    ''')

    # Inserimento degli utenti (4 vulnerabili e uno sicuro)
    users = [
        (1, 'PizzaioloAdmin69', 'S&F4thewin', 'db_utenti_steg.html'),
        (2, 'HINT', 'HINT', 'HINT.html'),
        (3, 'Oznerol', 'Oznerol','Oznerol.html'),
        (4, 'Annavoigairam', 'Annavoigairam', 'Annavoigairam.html'),
        (5, 'brain', 'heart', 'secure_user.html'),
    ]
    
    # Salva i cambiamenti
    c.executemany("INSERT OR IGNORE INTO users (id, username, password, dashboard_file) VALUES (?, ?, ?, ?)", users)
    conn.commit()
    conn.close()

# Funzione di login
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Debug: Stampa credenziali ricevute
        print(f"[DEBUG] Tentativo di login: Username: {username}, Password: {password}")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()



        try:
            if username == "brain":
                # Query sicura per l'utente protetto
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            else:
                # Query vulnerabile costruita manualmente
                query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
                print(f"[DEBUG] Query eseguita: {query}")
                c.execute(query)
                
            user = c.fetchone()#modificato
        except sqlite3.OperationalError as e:
            print(f"[DEBUG] Errore SQL: {e}")
            user = None

        conn.close()

        if user:
            return redirect(url_for("user_dashboard", username=user[1]))
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

''''@app.route("/read", methods=["GET", "POST"])
def read_file():
    if request.method == "POST":
        filename = request.form.get("file")
        if not filename:
            return render_template("read.html", error="Specifica un file!")

        # Verifica del percorso del file
        filepath = os.path.join(BASE_DIR, filename)
        try:
            if not filepath.startswith(BASE_DIR):  # Protezione contro Directory Traversal
                return render_template("read.html", error="Accesso negato!")

            # Leggi il contenuto del file e visualizzalo nella pagina
            with open(filepath, "r") as f:
                content = f.read()
            return render_template("read.html", content=content)
        except FileNotFoundError:
            return render_template("read.html", error="File non trovato!")
    return render_template("read.html")'''

if __name__ == "__main__":
    init_db()
    app.run(debug=True,host="0.0.0.0", port=5000)
    

