"""Tests d'intégration pour les endpoints de l'API articles.

Ce module contient tous les tests pour vérifier le bon fonctionnement
des opérations CRUD sur les articles via l'API FastAPI.
"""

import pytest
from fastapi.testclient import TestClient


def test_create_item(client: TestClient):
    """Teste la création d'un article valide."""
    response = client.post(
        "/items/",
        json={"nom": "Test Item", "prix": 19.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Test Item"
    assert data["prix"] == 19.99
    assert "id" in data


def test_create_item_invalid_price(client: TestClient):
    """Teste que la création échoue avec un prix négatif."""
    response = client.post(
        "/items/",
        json={"nom": "Test Item", "prix": -10}
    )
    assert response.status_code == 422


def test_create_item_empty_name(client: TestClient):
    """Teste que la création échoue avec un nom vide."""
    response = client.post(
        "/items/",
        json={"nom": "", "prix": 10}
    )
    assert response.status_code == 422


def test_get_items_empty(client: TestClient):
    """Teste la récupération d'une liste vide d'articles."""
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_items(client: TestClient):
    """Teste la récupération de plusieurs articles."""
    client.post("/items/", json={"nom": "Item 1", "prix": 10.0})
    client.post("/items/", json={"nom": "Item 2", "prix": 20.0})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nom"] == "Item 1"
    assert data[1]["nom"] == "Item 2"


def test_get_item_by_id(client: TestClient):
    """Teste la récupération d'un article spécifique par son ID."""
    create_response = client.post(
        "/items/",
        json={"nom": "Test Item", "prix": 15.0}
    )
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["nom"] == "Test Item"
    assert data["prix"] == 15.0


def test_get_item_not_found(client: TestClient):
    """Teste que la récupération d'un article inexistant retourne 404."""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_item(client: TestClient):
    """Teste la mise à jour complète d'un article."""
    create_response = client.post(
        "/items/",
        json={"nom": "Original", "prix": 10.0}
    )
    item_id = create_response.json()["id"]

    update_response = client.put(
        f"/items/{item_id}",
        json={"nom": "Updated", "prix": 25.0}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["nom"] == "Updated"
    assert data["prix"] == 25.0


def test_update_item_partial(client: TestClient):
    """Teste la mise à jour partielle d'un article (uniquement le prix)."""
    create_response = client.post(
        "/items/",
        json={"nom": "Original", "prix": 10.0}
    )
    item_id = create_response.json()["id"]

    update_response = client.put(
        f"/items/{item_id}",
        json={"prix": 30.0}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["nom"] == "Original"
    assert data["prix"] == 30.0


def test_update_item_not_found(client: TestClient):
    """Teste que la mise à jour d'un article inexistant retourne 404."""
    response = client.put(
        "/items/999",
        json={"nom": "Updated", "prix": 25.0}
    )
    assert response.status_code == 404


def test_delete_item(client: TestClient):
    """Teste la suppression d'un article existant."""
    create_response = client.post(
        "/items/",
        json={"nom": "To Delete", "prix": 10.0}
    )
    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client: TestClient):
    """Teste que la suppression d'un article inexistant retourne 404."""
    response = client.delete("/items/999")
    assert response.status_code == 404


def test_pagination(client: TestClient):
    """Teste la pagination avec skip et limit."""
    for i in range(15):
        client.post("/items/", json={"nom": f"Item {i}", "prix": float(i + 1)})

    response = client.get("/items/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["nom"] == "Item 5"


def test_health_endpoint(client: TestClient):
    """Teste l'endpoint de vérification de santé de l'API."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client: TestClient):
    """Teste l'endpoint racine de l'API."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
