"""Points de terminaison API pour la gestion des articles.

Ce module définit toutes les routes FastAPI pour les opérations CRUD
sur les articles. Les routes utilisent ItemService pour la logique métier.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste des articles avec pagination.

    Args:
        skip: Nombre d'articles à sauter (offset). Par défaut 0.
        limit: Nombre maximum d'articles à retourner. Par défaut 100.
        db: Session de base de données (injectée automatiquement).

    Returns:
        Liste des articles sous forme de schémas ItemResponse.

    Example:
        GET /items/?skip=0&limit=10
    """
    return ItemService.get_all(db, skip, limit)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Récupère un article spécifique par son ID.

    Args:
        item_id: Identifiant unique de l'article recherché.
        db: Session de base de données (injectée automatiquement).

    Returns:
        L'article trouvé sous forme de schéma ItemResponse.

    Raises:
        HTTPException: 404 si l'article n'existe pas.

    Example:
        GET /items/1
    """
    item = ItemService.get_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    """Crée un nouvel article dans la base de données.

    Args:
        item_data: Données de l'article à créer (schéma ItemCreate validé).
        db: Session de base de données (injectée automatiquement).

    Returns:
        L'article créé avec son ID généré (schéma ItemResponse).

    Example:
        POST /items/
        Body: {"nom": "Laptop", "prix": 899.99}
    """
    return ItemService.create(db, item_data)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    """Met à jour un article existant.

    Effectue une mise à jour partielle : seuls les champs fournis
    dans item_data seront modifiés.

    Args:
        item_id: Identifiant de l'article à mettre à jour.
        item_data: Nouvelles données (schéma ItemUpdate avec champs optionnels).
        db: Session de base de données (injectée automatiquement).

    Returns:
        L'article mis à jour (schéma ItemResponse).

    Raises:
        HTTPException: 404 si l'article n'existe pas.

    Example:
        PUT /items/1
        Body: {"prix": 799.99}  # Met à jour seulement le prix
    """
    item = ItemService.update(db, item_id, item_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Supprime un article de la base de données.

    Args:
        item_id: Identifiant de l'article à supprimer.
        db: Session de base de données (injectée automatiquement).

    Returns:
        Aucun contenu (status 204 No Content) en cas de succès.

    Raises:
        HTTPException: 404 si l'article n'existe pas.

    Example:
        DELETE /items/1
    """
    deleted = ItemService.delete(db, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
