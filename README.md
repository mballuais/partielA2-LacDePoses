# 🏞️ Parc d'Activité du Lac de Poses - Location de Matériel

Application web de gestion de location de matériel développée avec Flask.

## 🛠️ Stack Technique

- **Framework Backend** : Flask (Python)
- **ORM** : SQLAlchemy
- **Migrations** : Flask-Migrate
- **Templates** : Jinja2
- **Base de données** : SQLite
- **Frontend** : Bootstrap 5 + Font Awesome

## 📦 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner et accéder au projet**
```bash
git clone <votre-repo>
cd location-materiel
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Initialiser la base de données**
```bash
flask db upgrade
```

5. **Ajouter des données de test (optionnel)**
```bash
python seed_data.py
```

6. **Lancer l'application**
```bash
python run.py
```

L'application sera accessible sur **http://127.0.0.1:5000**

## 🗂️ Structure du Projet

```
location-materiel/
├── app/
│   ├── __init__.py              # Configuration Flask
│   ├── models.py                # Modèles de données
│   ├── routes.py                # Routes et logique
│   ├── templates/               # Templates HTML
│   └── static/                  # Fichiers statiques
├── migrations/                  # Migrations base de données
├── config.py                    # Configuration
├── run.py                       # Point d'entrée
├── seed_data.py                 # Données de test
└── requirements.txt             # Dépendances
```

## ⚡ Fonctionnalités

- **Gestion du matériel** : Ajout, modification
- **Commandes** : Création et gestion complète
- **Stocks** : Suivi automatique des quantités
- **Restitution** : Retour du matériel loué
- **Recherche** : Filtrage temps réel
- **Statistiques** : Tableau de bord
- **Interface responsive** : Bootstrap + icônes

## 🔧 Utilisation

1. Ajoutez du matériel via "Ajouter Matériel"
2. Créez des commandes pour vos clients
3. Gérez les stocks automatiquement
4. Consultez les statistiques dans le dashboard

## 💾 Base de Données

### Modèles principaux
- **Material** : Matériel avec nom, quantité, prix
- **Order** : Commande avec client et prix total
- **OrderItem** : Liaison matériel-commande

---

**Application développée pour le parc d'activité du lac de Poses**