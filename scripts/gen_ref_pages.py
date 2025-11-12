"""Script de génération automatique de la référence API.

Ce script scanne tous les modules Python dans le dossier 'app/'
et génère automatiquement des fichiers Markdown pour la documentation.

Exécuté automatiquement par MkDocs pendant le build grâce au plugin mkdocs-gen-files.
"""

from pathlib import Path

import mkdocs_gen_files

# Dossier racine du code source à documenter
SOURCE_DIR = Path("app")

# Dossier où seront générés les fichiers markdown (virtuel, pas sur disque)
DOCS_DIR = "reference"

# Liste pour collecter tous les fichiers générés
nav_items = []

# Parcourir récursivement tous les fichiers .py dans app/
for path in sorted(SOURCE_DIR.rglob("*.py")):
    # Ignorer les dossiers __pycache__ et fichiers temporaires
    if "__pycache__" in str(path):
        continue

    # Construire le chemin du module Python (ex: app/models/item.py → app/models/item)
    module_path = path.relative_to(".").with_suffix("")

    # Construire le chemin du fichier markdown de destination
    # Ex: reference/app/models/item.md
    doc_path = Path(DOCS_DIR) / path.relative_to(".").with_suffix(".md")

    # Convertir en notation pointée pour l'import Python
    # Path("app/models/item") → "app.models.item"
    parts = list(module_path.parts)

    # Gestion spéciale pour __init__.py
    if parts[-1] == "__init__":
        # Pour __init__.py, on documente le package entier
        parts = parts[:-1]
        # Créer un fichier avec le nom du package
        if len(parts) > 0:
            doc_path = (
                Path(DOCS_DIR) / "/".join(parts[:-1]) / f"{parts[-1]}.md"
                if len(parts) > 1
                else Path(DOCS_DIR) / f"{parts[0]}.md"
            )
        else:
            continue  # Ignorer si pas de partie valide

    # Nom du module en notation Python (ex: "app.models.item")
    module_name = ".".join(parts)

    # Ignorer si le nom de module est vide
    if not module_name:
        continue

    # Créer le fichier markdown virtuel avec mkdocs_gen_files
    with mkdocs_gen_files.open(doc_path, "w") as f:
        # Écrire l'en-tête du fichier
        print(f"# `{module_name}`", file=f)
        print(file=f)

        # Écrire la directive mkdocstrings pour générer automatiquement la doc
        print(f"::: {module_name}", file=f)
        print("    options:", file=f)
        print("      show_root_heading: false", file=f)  # On a déjà le titre ci-dessus
        print("      show_source: true", file=f)
        print("      heading_level: 2", file=f)

    # Enregistrer la source du fichier pour permettre le lien "Edit on GitHub"
    mkdocs_gen_files.set_edit_path(doc_path, path)

    # Ajouter à la liste de navigation
    nav_items.append((module_name, doc_path))

# Générer le fichier SUMMARY.md pour la navigation (APRÈS la boucle)
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.write("# Référence API\n\n")

    # Organiser par modules de premier niveau
    current_module = None
    for module_name, doc_path in sorted(nav_items):
        parts = module_name.split(".")

        # Calculer le chemin relatif depuis reference/SUMMARY.md
        # doc_path est comme "reference/app/database.md"
        # On veut "app/database.md" (relatif à reference/)
        relative_path = str(doc_path).replace("reference/", "")

        # Module de premier niveau (ex: "app")
        if len(parts) == 1:
            nav_file.write(f"* [{module_name}]({relative_path})\n")
        # Sous-module de deuxième niveau (ex: "app.database")
        elif len(parts) == 2:
            nav_file.write(f"    * [{parts[1]}]({relative_path})\n")
        # Sous-module de troisième niveau (ex: "app.models.item")
        elif len(parts) == 3:
            if current_module != parts[1]:
                current_module = parts[1]
            nav_file.write(f"        * [{parts[2]}]({relative_path})\n")

print("✅ Génération automatique de la référence API terminée")
