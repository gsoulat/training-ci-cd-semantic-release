"""Configuration de la base de données et gestion des sessions.

Ce module gère la connexion à la base de données PostgreSQL
et fournit une fonction générateur pour obtenir des sessions de base de données.
"""

from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/items_db"
)

engine = create_engine(DATABASE_URL)


def get_db():
    """Générateur de session de base de données pour FastAPI.

    Crée et gère une session de base de données SQLModel.
    La session est automatiquement fermée après utilisation.

    Yields:
        Session: Session SQLModel active pour les opérations de base de données.

    Example:
        >>> from fastapi import Depends
        >>> def my_route(db: Session = Depends(get_db)):
        ...     # Utiliser la session db ici
        ...     pass
    """
    with Session(engine) as session:
        yield session
