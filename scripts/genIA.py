"""Script de génération de documentation par IA avec OpenRouter.

Ce script scanne tous les modules Python dans le dossier 'app/'
et génère automatiquement des guides d'utilisation détaillés
en utilisant l'API OpenRouter.ai.

Exécuté automatiquement par MkDocs pendant le build grâce au plugin mkdocs-gen-files.

Peut être exécuté en local (sans clé API = mode placeholder) ou
dans le workflow GitHub Actions (avec clé API = génération réelle).
"""

import os
from pathlib import Path

import mkdocs_gen_files
import requests

# Configuration OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
USE_AI = bool(OPENROUTER_API_KEY)

if not USE_AI:
    print("⚠️  Variable d'environnement OPENROUTER_API_KEY non définie")
    print("📝 Mode PLACEHOLDER : génération de docs minimales sans IA")

# Dossier racine du code source à documenter
SOURCE_DIR = Path("app")

# Dossier où seront générés les fichiers markdown (virtuel, pas sur disque)
DOCS_DIR = "docsIA"

# Liste pour collecter tous les guides générés
nav_items = []

# Modèle OpenRouter à utiliser pour la génération
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"


def generate_placeholder(module_name: str) -> str:
    """Génère un placeholder simple pour le mode sans IA.

    Args:
        module_name: Nom du module Python (ex: "app.database")

    Returns:
        Documentation placeholder en format Markdown
    """
    return f"""# Guide : {module_name}

> ⚠️ Ce guide est un placeholder généré en mode développement local.
> La documentation complète sera générée lors du déploiement avec l'IA.

## À propos de ce module

Ce module fait partie du projet Items CRUD API.

Pour voir la référence technique détaillée, consultez la section **Référence API**.

---

**Note** : Cette page sera automatiquement remplacée par un guide détaillé
généré par IA lors du déploiement sur GitHub Pages.
"""


def generate_guide_with_ai(module_name: str, source_code: str) -> str:
    """Génère un guide d'utilisation détaillé avec l'API OpenRouter.

    Args:
        module_name: Nom du module Python (ex: "app.database")
        source_code: Code source du module

    Returns:
        Guide d'utilisation en format Markdown
    """
    # Mode placeholder si pas de clé API
    if not USE_AI:
        return generate_placeholder(module_name)

    # Prompt système pour la génération
    system_prompt = """Tu es un expert en documentation technique Python.
Ta tâche est de créer des guides d'utilisation détaillés, pédagogiques et pratiques.

Pour chaque module fourni, génère un guide qui contient :
1. **Vue d'ensemble** : Description du rôle et de la responsabilité du module
2. **Concepts clés** : Explications des concepts importants utilisés
3. **Guide d'utilisation** : Exemples concrets d'utilisation pas-à-pas
4. **Cas d'usage courants** : Scénarios réels avec code complet
5. **Bonnes pratiques** : Recommandations pour utiliser ce module correctement
6. **Pièges à éviter** : Erreurs communes et comment les éviter

Le guide doit être :
- Pédagogique et accessible aux débutants
- Riche en exemples de code concrets et exécutables
- Structuré avec des titres Markdown clairs
- Orienté pratique plutôt que théorique
"""

    user_prompt = f"""Génère un guide d'utilisation détaillé pour ce module Python :

Module : {module_name}

Code source :
```python
{source_code}
```

Génère un guide complet en français, au format Markdown."""

    # Appel à l'API OpenRouter
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()

        guide_content = data["choices"][0]["message"]["content"]
        return guide_content

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de l'appel à OpenRouter pour {module_name}: {e}")
        return f"# {module_name}\n\n⚠️ Erreur lors de la génération du guide."


# Parcourir récursivement tous les fichiers .py dans app/
for path in sorted(SOURCE_DIR.rglob("*.py")):
    # Ignorer les dossiers __pycache__ et fichiers temporaires
    if "__pycache__" in str(path):
        continue

    # Construire le nom du module
    module_path = path.relative_to(".").with_suffix("")
    parts = list(module_path.parts)

    # Gestion spéciale pour __init__.py
    if parts[-1] == "__init__":
        parts = parts[:-1]
        if len(parts) == 0:
            continue

    module_name = ".".join(parts)
    if not module_name:
        continue

    print(f"📄 Génération du guide pour : {module_name}")

    # Lire le code source
    source_code = path.read_text(encoding="utf-8")

    # Générer le guide avec l'IA
    guide_content = generate_guide_with_ai(module_name, source_code)

    # Créer le chemin du fichier markdown de destination
    doc_filename = f"{parts[-1]}.md" if parts else "module.md"

    # Construire le chemin du fichier markdown (ex: docsIA/models/item.md)
    if len(parts) > 1:
        # Sous-module : créer dans un sous-dossier
        doc_path = Path(DOCS_DIR) / parts[1] / doc_filename if len(parts) > 1 else Path(DOCS_DIR) / doc_filename
    else:
        doc_path = Path(DOCS_DIR) / doc_filename

    # Créer le fichier markdown virtuel avec mkdocs_gen_files
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(guide_content)

    # Enregistrer la source du fichier pour permettre le lien "Edit on GitHub"
    mkdocs_gen_files.set_edit_path(doc_path, path)

    # Calculer le chemin relatif pour la navigation
    relative_path = str(doc_path).replace(f"{DOCS_DIR}/", "")
    nav_items.append((module_name, relative_path))

# Générer le fichier SUMMARY.md pour la navigation (APRÈS la boucle)
with mkdocs_gen_files.open(f"{DOCS_DIR}/SUMMARY.md", "w") as nav_file:
    nav_file.write("# Documentation générée par IA\n\n")
    nav_file.write("Cette section contient des guides d'utilisation détaillés ")
    nav_file.write("générés automatiquement par intelligence artificielle.\n\n")
    nav_file.write("## Guides disponibles\n\n")

    # Organiser par modules de premier niveau
    for module_name, doc_path in sorted(nav_items):
        parts = module_name.split(".")

        # Module de premier niveau (ex: "app")
        if len(parts) == 1:
            nav_file.write(f"* [{module_name}]({doc_path})\n")
        # Sous-module de deuxième niveau (ex: "app.database")
        elif len(parts) == 2:
            nav_file.write(f"    * [{parts[1]}]({doc_path})\n")
        # Sous-module de troisième niveau (ex: "app.models.item")
        elif len(parts) == 3:
            nav_file.write(f"        * [{parts[2]}]({doc_path})\n")

print(f"✅ Génération automatique de la documentation IA terminée ({len(nav_items)} guides)")
