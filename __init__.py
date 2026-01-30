from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

def current_client_id():
    return session.get("user_id")

@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livres")
    livres = cursor.fetchall()

    conn.close()

    return render_template("livres.html", livres=livres)

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    adresse = request.form['adresse'] 

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, adresse))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement


@app.route("/login_user", methods=["GET", "POST"])
def login_user():
    error = False

    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, role FROM users WHERE login = ? AND password = ?",
            (login, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]   # ID utilisateur
            session["role"] = user[1]      # user / admin
            session["login"] = login       # ✅ AJOUT ICI
            return redirect(url_for("livres"))
        else:
            error = True

    return render_template("login_user.html", error=error)



@app.route("/fiche_nom/", methods=["GET"])
def fiche_nom():
    nom = request.args.get("nom")

    data = None
    if nom:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM clients WHERE nom = ?",
            (nom,)
        )
        data = cursor.fetchall()
        conn.close()

    return render_template("fiche_nom.html", data=data, nom=nom)

# PROJET BIBLIOTHEQUE 

@app.route("/api/livres", methods=["GET"])
def api_livres():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, titre, auteur, stock FROM livres")
    livres = cursor.fetchall()
    conn.close()

    result = []
    for livre in livres:
        result.append({
            "id": livre["id"],
            "titre": livre["titre"],
            "auteur": livre["auteur"],
            "stock": livre["stock"]
        })

    return jsonify(result)

@app.route("/livres", methods=["GET"])
def livres():
    if not current_client_id():
        return redirect(url_for("login_user"))
    
    q = request.args.get("q", "")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if q:
        cursor.execute("""
            SELECT * FROM livres
            WHERE stock > 0
            AND (titre LIKE ? OR auteur LIKE ?)
        """, (f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT * FROM livres WHERE stock > 0")

    livres = cursor.fetchall()
    conn.close()

    return render_template("livres.html", livres=livres, q=q)

# Recherche de livre

@app.route("/api/livres/search", methods=["GET"])
def api_search_livres():
    q = request.args.get("q", "")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM livres
        WHERE stock > 0
        AND (titre LIKE ? OR auteur LIKE ?)
    """, (f"%{q}%", f"%{q}%"))

    livres = cursor.fetchall()
    conn.close()

    return jsonify([dict(livre) for livre in livres])

# Emprunter un livre 

@app.route("/api/emprunter", methods=["POST"])
def emprunter_livre():
    client_id = current_client_id()
    livre_id = request.form.get("livre_id")

    if not client_id:
        return redirect(url_for("login_user"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Vérifier le stock
    cursor.execute(
        "SELECT stock FROM livres WHERE id = ?",
        (livre_id,)
    )
    stock = cursor.fetchone()

    if not stock or stock[0] <= 0:
        conn.close()
        return "Livre indisponible", 400

    # Enregistrer l’emprunt
    cursor.execute(
        "INSERT INTO emprunts (livre_id, client_id) VALUES (?, ?)",
        (livre_id, client_id)
    )

    # Diminuer le stock
    cursor.execute(
        "UPDATE livres SET stock = stock - 1 WHERE id = ?",
        (livre_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("livres"))

# Restiuer un livre emprunté 

@app.route("/api/restituer", methods=["POST"])
def restituer_livre():
    client_id = current_client_id()
    emprunt_id = request.form.get("emprunt_id")

    if not client_id:
        return redirect(url_for("login_user"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # récupérer le livre lié à l’emprunt
    cursor.execute(
        "SELECT livre_id FROM emprunts WHERE id = ? AND client_id = ?",
        (emprunt_id, client_id)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        return "Emprunt introuvable", 404

    livre_id = row[0]

    # supprimer l’emprunt
    cursor.execute(
        "DELETE FROM emprunts WHERE id = ?",
        (emprunt_id,)
    )

    # remettre le stock
    cursor.execute(
        "UPDATE livres SET stock = stock + 1 WHERE id = ?",
        (livre_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("mes_emprunts"))


# Consulter ses emprunts 

@app.route("/mes_emprunts")
def mes_emprunts():
    client_id = current_client_id()

    if not client_id:
        return redirect(url_for("login_user"))

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e.id AS emprunt_id,
            l.titre,
            l.auteur
        FROM emprunts e
        JOIN livres l ON l.id = e.livre_id
        WHERE e.client_id = ?
    """, (client_id,))

    emprunts = cursor.fetchall()
    conn.close()

    return render_template("mes_emprunts.html", emprunts=emprunts)



# Ajouter des livres à la liste 

@app.route("/livres/ajouter", methods=["GET", "POST"])
def ajouter_livre():
    if request.method == "POST":
        titre = request.form.get("titre")
        auteur = request.form.get("auteur")
        stock = request.form.get("stock")

        if not titre or not auteur or not stock:
            return "Champs manquants", 400

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)",
            (titre, auteur, int(stock))
        )

        conn.commit()
        conn.close()

        return redirect(url_for("livres"))

    # GET → afficher le formulaire
    return render_template("ajouter_livre.html")

if __name__ == "__main__":
    app.run(debug=True)
