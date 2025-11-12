# Bienvenue dans la documentation Items CRUD API

## 🎯 Vue d'ensemble

Cette API FastAPI permet de gérer une liste d'articles avec les opérations CRUD complètes :
- **C**reate : Créer de nouveaux articles
- **R**ead : Lire/consulter les articles
- **U**pdate : Modifier des articles existants
- **D**elete : Supprimer des articles

## 🏗️ Architecture

Le projet suit une architecture en couches propre :

```
app/
├── main.py          # Application FastAPI principale
├── database.py      # Configuration base de données
├── models/          # Modèles SQLModel (ORM)
├── schemas/         # Validation Pydantic
├── services/        # Logique métier
└── routes/          # Endpoints API REST
```

## 📖 Navigation

- **[Référence API](reference.md)** - Documentation complète auto-générée de tous les modules
- **[Tutoriel MkDocs](tutoriel-mkdocs.md)** - Comprendre comment fonctionne cette documentation

## 🚀 Démarrage rapide

### Installation

```bash
# Installer les dépendances
uv sync

# Démarrer PostgreSQL avec Docker
docker-compose up -d

# Démarrer l'API
uv run uvicorn app.main:app --reload
```

### Générer cette documentation

```bash
# Serveur de développement (avec auto-reload)
uv run mkdocs serve

# Construire les fichiers HTML
uv run mkdocs build
```

## 📚 Aperçu des modules principaux

Voici un aperçu de deux modules clés de l'application.

### Configuration de la base de données

::: app.database.get_db
    options:
      show_root_heading: false
      show_source: false

### Modèle Item

::: app.models.item.Item
    options:
      show_root_heading: false
      show_source: false