"""Schémas Pydantic pour la validation des données d'articles.

Ce module contient les schémas utilisés pour valider les données
des requêtes et réponses de l'API concernant les articles.
"""

from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    """Schéma de base contenant les champs communs d'un article.

    Cette classe définit les attributs partagés entre les différents
    schémas d'articles (création, mise à jour, réponse).

    Attributes:
        nom: Nom de l'article (1-255 caractères).
        prix: Prix de l'article (doit être strictement positif).
    """

    nom: str = Field(min_length=1, max_length=255)
    prix: float = Field(gt=0)


class ItemCreate(ItemBase):
    """Schéma pour la création d'un nouvel article.

    Hérite de ItemBase et ne nécessite pas d'ID (généré automatiquement).
    Utilisé lors de la requête POST /items/.

    Example:
        >>> item_data = ItemCreate(nom="Clavier", prix=49.99)
    """

    pass


class ItemUpdate(SQLModel):
    """Schéma pour la mise à jour partielle d'un article existant.

    Tous les champs sont optionnels pour permettre des mises à jour partielles.
    Utilisé lors de la requête PUT /items/{item_id}.

    Attributes:
        nom: Nouveau nom de l'article (optionnel, 1-255 caractères si fourni).
        prix: Nouveau prix de l'article (optionnel, doit être positif si fourni).

    Example:
        >>> # Mise à jour uniquement du prix
        >>> update_data = ItemUpdate(prix=39.99)
    """

    nom: str | None = Field(None, min_length=1, max_length=255)
    prix: float | None = Field(None, gt=0)


class ItemResponse(ItemBase):
    """Schéma pour la réponse API contenant un article.

    Hérite de ItemBase et ajoute l'ID généré par la base de données.
    Utilisé pour toutes les réponses renvoyant un ou plusieurs articles.

    Attributes:
        id: Identifiant unique de l'article.
        nom: Nom de l'article (hérité de ItemBase).
        prix: Prix de l'article (hérité de ItemBase).

    Example:
        >>> response = ItemResponse(id=1, nom="Souris", prix=29.99)
    """

    id: int
