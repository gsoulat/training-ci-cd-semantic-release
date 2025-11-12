# Tutoriel : Générer de la documentation automatique avec MkDocs

## Introduction

MkDocs est un générateur de documentation statique conçu pour créer des documentations de projets à partir de fichiers Markdown. Combiné avec **mkdocstrings**, il permet de générer automatiquement la documentation API à partir des docstrings Python.

## Pourquoi MkDocs + mkdocstrings ?

### Avantages
- ✅ **Simple** : Configuration YAML facile à comprendre
- ✅ **Moderne** : Theme Material avec interface élégante et responsive
- ✅ **Auto-génération** : Extrait la documentation depuis les docstrings Python
- ✅ **FastAPI-friendly** : Utilisé par la communauté FastAPI
- ✅ **Recherche intégrée** : Recherche full-text automatique
- ✅ **Support Google docstrings** : Compatible avec le format que nous utilisons

### Architecture

```
projet/
├── docs/                    # Dossier contenant les fichiers Markdown
│   ├── index.md            # Page d'accueil
│   ├── reference.md        # Référence API auto-générée
│   └── tutoriel-mkdocs.md  # Ce tutoriel
├── mkdocs.yml              # Fichier de configuration principal
└── app/                    # Code source Python avec docstrings
    ├── main.py
    ├── database.py
    ├── models/
    ├── schemas/
    ├── services/
    └── routes/
```

## Fonctionnement de mkdocstrings

### La directive `:::`

C'est la syntaxe spéciale qui indique à mkdocstrings de générer automatiquement la documentation :

```markdown
::: nom_du_module.nom_de_la_classe_ou_fonction
    options:
      show_root_heading: true
      show_source: true
```

**Ce qui se passe :**
1. MkDocs lit cette directive
2. mkdocstrings **importe** le module Python spécifié
3. Il extrait les docstrings (descriptions, paramètres, retours)
4. Il génère du HTML formaté avec la documentation

### Exemple concret

Si vous écrivez dans `docs/reference.md` :

```markdown
## Module Database

::: app.database
```

MkDocs va :
1. Importer `app.database`
2. Extraire les docstrings de `get_db()` et des variables
3. Créer une section HTML avec :
   - Description du module
   - Signature de la fonction `get_db()`
   - Paramètres, types, valeurs de retour
   - Exemples dans la docstring

## Configuration : mkdocs.yml

### Structure du fichier

```yaml
site_name: Ma Documentation        # Titre du site

theme:
  name: material                   # Theme moderne Material Design

plugins:
  - search                         # Plugin de recherche
  - mkdocstrings:                  # Plugin pour auto-génération
      handlers:
        python:                    # Handler pour code Python
          options:
            docstring_style: google    # Format des docstrings
            show_source: true          # Afficher le code source
            show_root_heading: true    # Afficher le titre principal

nav:                               # Menu de navigation
  - Accueil: index.md
  - Référence API: reference.md
  - Tutoriel MkDocs: tutoriel-mkdocs.md
```

### Options importantes pour Python

| Option | Valeur | Description |
|--------|--------|-------------|
| `docstring_style` | `google`, `numpy`, `sphinx` | Format des docstrings à parser |
| `show_source` | `true`/`false` | Afficher le code source des fonctions |
| `show_root_heading` | `true`/`false` | Afficher le nom du module/classe en titre |
| `show_root_toc_entry` | `true`/`false` | Ajouter dans la table des matières |
| `heading_level` | `1`-`6` | Niveau des titres HTML générés |
| `members_order` | `source`, `alphabetical` | Ordre des membres de classe |

## Créer la documentation

### Étape 1 : Préparer index.md (Page d'accueil)

Le fichier `docs/index.md` est la page d'accueil de votre documentation.

**Exemple de structure :**

```markdown
# Bienvenue dans la documentation Items CRUD API

## Vue d'ensemble

Cette API FastAPI permet de gérer une liste d'articles avec les opérations CRUD complètes.

## Architecture

Le projet suit une architecture en couches :

- **Routes** (`app.routes`) : Endpoints FastAPI
- **Services** (`app.services`) : Logique métier
- **Models** (`app.models`) : Modèles de base de données SQLModel
- **Schemas** (`app.schemas`) : Validation Pydantic

## Modules principaux

Voici un aperçu des modules principaux avec leur documentation auto-générée :

### Database
::: app.database
    options:
      show_root_heading: false
      show_source: false

### Models
::: app.models.item
    options:
      show_root_heading: false
```

### Étape 2 : Créer reference.md (Référence API complète)

Le fichier `docs/reference.md` contient la documentation API détaillée de tous vos modules.

**Structure recommandée :**

```markdown
# Référence API

Documentation complète de tous les modules du projet.

## Database

::: app.database
    options:
      show_root_heading: true
      show_source: true

## Models

### Item
::: app.models.item
    options:
      show_root_heading: true
      show_source: true

## Schemas

::: app.schemas.item
    options:
      show_root_heading: true
      show_source: true

## Services

::: app.services.item_service
    options:
      show_root_heading: true
      show_source: true

## Routes

::: app.routes.items
    options:
      show_root_heading: true
      show_source: true

## Application principale

::: app.main
    options:
      show_root_heading: true
      show_source: true
```

### Étape 3 : Construire et prévisualiser

#### Serveur de développement (avec rechargement automatique)

```bash
uv run mkdocs serve
```

Ouvre http://127.0.0.1:8000 dans votre navigateur. La documentation se recharge automatiquement quand vous modifiez les fichiers.

#### Construire les fichiers HTML statiques

```bash
uv run mkdocs build
```

Génère le site dans le dossier `site/`. Vous pouvez déployer ces fichiers sur n'importe quel serveur web.

#### Options de build utiles

```bash
# Build avec mode strict (échoue sur warnings)
uv run mkdocs build --strict

# Nettoyer avant de builder
uv run mkdocs build --clean

# Verbose (afficher plus de détails)
uv run mkdocs build --verbose
```

## Dépannage

### Erreur : "No module named 'mon_package'"

**Problème** : mkdocstrings essaie d'importer un module qui n'existe pas.

**Solution** : Vérifiez les directives `:::` dans vos fichiers Markdown. Le chemin doit correspondre à votre structure de code :
- ✅ Correct : `::: app.database`
- ❌ Incorrect : `::: mon_package.mon_module`

### Erreur : "A reference to 'reference.md' is included in nav"

**Problème** : Le fichier `reference.md` est référencé dans `mkdocs.yml` mais n'existe pas.

**Solution** : Créez le fichier `docs/reference.md` ou retirez-le de la navigation.

### Documentation vide ou incomplète

**Causes possibles** :
1. **Pas de docstrings** : Vérifiez que vos fonctions/classes ont des docstrings
2. **Format incorrect** : Vérifiez que `docstring_style: google` correspond à vos docstrings
3. **Module non importable** : Vérifiez que Python peut importer votre module

**Test d'import :**
```bash
# Tester si le module est importable
uv run python -c "import app.database; print('OK')"
```

### Warning : "Document not included in any toctree"

**Problème** : Des fichiers `.rst` ou `.md` existent mais ne sont pas référencés dans la navigation.

**Solution** : Ajoutez-les dans `nav:` de `mkdocs.yml` ou ignorez-les avec `exclude_docs:`.

## Personnalisation avancée

### Theme Material - Configuration étendue

```yaml
theme:
  name: material
  palette:
    - scheme: default              # Mode clair
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate                # Mode sombre
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs              # Onglets de navigation
    - navigation.sections          # Sections dans le menu
    - navigation.expand            # Expand automatique
    - navigation.top               # Bouton retour en haut
    - search.suggest               # Suggestions de recherche
    - search.highlight             # Surligner les résultats
    - content.code.copy            # Bouton copier pour code
```

### Filtrer les membres d'une classe

```markdown
::: app.models.item.Item
    options:
      show_root_heading: true
      members:
        - __init__
        - nom
        - prix
      filters:
        - "!^_"          # Exclure les attributs privés
```

### Regrouper par catégories

```markdown
## Services

### ItemService

#### Opérations de lecture
::: app.services.item_service.ItemService.get_all
::: app.services.item_service.ItemService.get_by_id

#### Opérations d'écriture
::: app.services.item_service.ItemService.create
::: app.services.item_service.ItemService.update
::: app.services.item_service.ItemService.delete
```

## Bonnes pratiques

### 1. Structure de documentation claire

```
docs/
├── index.md              # Vue d'ensemble + getting started
├── reference.md          # API reference complète
├── guides/              # Guides utilisateur
│   ├── installation.md
│   └── quickstart.md
└── development/         # Guides développeurs
    ├── architecture.md
    └── contributing.md
```

### 2. Docstrings de qualité

- ✅ **DO** : Documenter tous les paramètres et retours
- ✅ **DO** : Ajouter des exemples concrets
- ✅ **DO** : Expliquer le "pourquoi", pas seulement le "quoi"
- ❌ **DON'T** : Docstrings génériques ("Cette fonction fait quelque chose")

### 3. Organisation de reference.md

- Regrouper par module logique (models, services, routes)
- Ordre logique : dependencies → models → services → routes
- Utiliser des titres clairs (## Markdown heading)

### 4. Configuration mkdocs.yml

- Commenter les options non-évidentes
- Tester régulièrement avec `mkdocs build --strict`
- Versionner le fichier de configuration

## Déploiement

### GitHub Pages

```bash
# Déployer automatiquement sur gh-pages
uv run mkdocs gh-deploy
```

### Netlify / Vercel

1. Connecter votre repo GitHub
2. Build command : `uv run mkdocs build`
3. Publish directory : `site/`

### Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /docs
COPY . .
RUN pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python
RUN mkdocs build
CMD ["python", "-m", "http.server", "8000", "-d", "site"]
```

## Ressources

- [Documentation MkDocs](https://www.mkdocs.org/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [mkdocstrings](https://mkdocstrings.github.io/)
- [mkdocstrings-python](https://mkdocstrings.github.io/python/)

## Conclusion

Avec MkDocs et mkdocstrings, vous obtenez :
- 🎨 Une documentation visuellement attractive
- 🤖 Génération automatique depuis le code
- 🔍 Recherche intégrée
- 📱 Interface responsive
- 🚀 Déploiement simple

La clé est d'écrire de bonnes docstrings dans votre code Python - le reste est automatique !
