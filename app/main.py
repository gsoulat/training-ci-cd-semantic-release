"""Application FastAPI principale pour l'API CRUD des articles.

Ce module initialise l'application FastAPI, configure les routes
et gère le cycle de vie de l'application (création des tables, etc.).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes import items_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Gestionnaire du cycle de vie de l'application FastAPI.

    Cette fonction est exécutée au démarrage et à l'arrêt de l'application.
    Elle crée toutes les tables de base de données au démarrage.

    Args:
        fastapi_app: Instance de l'application FastAPI.

    Yields:
        None: Permet l'exécution de l'application entre le démarrage et l'arrêt.
    """
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(items_router)


@app.get("/")
def root():
    """Point de terminaison racine de l'API.

    Returns:
        Message de bienvenue de l'API.

    Example:
        GET /
        Response: {"message": "Items CRUD API"}
    """
    return {"message": "Items CRUD API"}


@app.get("/health")
def health():
    """Vérification de l'état de santé de l'API.

    Point de terminaison utilisé pour les health checks
    (par exemple par les orchestrateurs de conteneurs).

    Returns:
        Statut de santé de l'application.

    Example:
        GET /health
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}


# @app.get("/mamie")
# def moliere():
#     return {
#         "citation": "Il faut manger pour vivre, et non pas vivre pour manger.",
#         "auteur": "Molière",
#         "oeuvre": "L'Avare",
#     }


secret ="fezffzefzefzlfzhfzfzfjzfzfzfdzgerg54g651fzefg51zeg5g"