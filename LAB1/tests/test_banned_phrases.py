def test_get_banned_phrases_empty(client):
    """Initially, the banned phrases list should be empty."""
    response = client.get("/api/v1/banned-phrases")
    assert response.status_code == 200
    assert response.json() == []


def test_create_banned_phrase_success(client):
    """Successfully adds a new banned phrase."""
    payload = {"name": "wulgaryzm"}
    response = client.post("/api/v1/banned-phrases", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data
    assert "created_at" in data


def test_create_duplicate_banned_phrase_fails(client):
    """Attempting to add a phrase with an existing name should return 400."""
    payload = {"name": "zakazane"}
    client.post("/api/v1/banned-phrases", json=payload)

    response = client.post("/api/v1/banned-phrases", json=payload)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_banned_phrase_name_validation(client):
    """Validates name length (minimum 3 characters) and invalid characters."""
    res_short = client.post("/api/v1/banned-phrases", json={"name": "ab"})
    assert res_short.status_code == 422

    res_chars = client.post("/api/v1/banned-phrases", json={"name": "fraza!@#"})
    assert res_chars.status_code == 422


def test_update_banned_phrase_success(client):
    """Successfully updates the name of an existing banned phrase."""
    res_create = client.post("/api/v1/banned-phrases", json={"name": "StaraFraza"})
    phrase_id = res_create.json()["id"]

    res_update = client.put(
        f"/api/v1/banned-phrases/{phrase_id}", json={"name": "NowaFraza"}
    )
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "NowaFraza"


def test_update_banned_phrase_to_taken_name_fails(client):
    """Cannot update a phrase name to one that already exists in the database."""
    client.post("/api/v1/banned-phrases", json={"name": "Pierwsza"})
    res2 = client.post("/api/v1/banned-phrases", json={"name": "Druga"})
    id2 = res2.json()["id"]

    res_update = client.put(f"/api/v1/banned-phrases/{id2}", json={"name": "Pierwsza"})
    assert res_update.status_code == 400
    assert "already taken" in res_update.json()["detail"]


def test_update_banned_phrase_not_found(client):
    """Updating a non-existent phrase returns 404."""
    response = client.put(
        "/api/v1/banned-phrases/99999", json={"name": "Nieistniejaca"}
    )
    assert response.status_code == 404


def test_delete_banned_phrase_success(client):
    """Successfully deletes an existing banned phrase."""
    res_create = client.post("/api/v1/banned-phrases", json={"name": "DoUsuniecia"})
    phrase_id = res_create.json()["id"]

    res_delete = client.delete(f"/api/v1/banned-phrases/{phrase_id}")
    assert res_delete.status_code == 200

    res_delete_again = client.delete(f"/api/v1/banned-phrases/{phrase_id}")
    assert res_delete_again.status_code == 404


def test_delete_banned_phrase_not_found(client):
    """Attempting to delete a non-existent phrase returns 404."""
    response = client.delete("/api/v1/banned-phrases/99999")
    assert response.status_code == 404
