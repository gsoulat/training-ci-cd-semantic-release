"""Modèles de base de données pour les articles.

Ce module définit les modèles SQLModel utilisés pour interagir
avec la table items dans la base de données.
"""

from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    """Modèle représentant un article dans la base de données.

    Cette classe définit la structure de la table 'items' et ses colonnes.
    Elle hérite de SQLModel pour permettre la validation Pydantic
    et la création automatique de la table.

    Attributes:
        id: Identifiant unique de l'article (clé primaire, auto-incrémenté).
        nom: Nom de l'article (indexé pour recherche rapide).
        prix: Prix de l'article en euros (doit être positif).

    Example:
        >>> item = Item(nom="Ordinateur", prix=999.99)
        >>> db.add(item)
        >>> db.commit()
    """

    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    nom: str = Field(index=True)
    prix: float
