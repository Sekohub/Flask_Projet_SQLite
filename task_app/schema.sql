CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT NOT NULL,
    date_echeance TEXT NOT NULL,
    terminee INTEGER DEFAULT 0
);

