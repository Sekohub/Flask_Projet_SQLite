import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# =========================
# CLIENTS
# =========================

cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris'))

# =========================
# USERS
# =========================
cur.execute("INSERT INTO users (login, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "admin"))
cur.execute("INSERT INTO users (login, password, role) VALUES (?, ?, ?)", ("user", "12345", "user"))

# =========================
# LIVRES
# =========================
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ("Python pour les nuls", "Dupont", 3))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ("Le Dit du Genji", "Murasaki", 2))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ("L'interprétation du rêve", "Freud", 1))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ("C pour les nuls", "Dan Gookin", 5))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ("Le Silmarillon", "Tolkien", 3))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ("Là où chantent les écrevisses", "Newman", 6))

connection.commit()
connection.close()
