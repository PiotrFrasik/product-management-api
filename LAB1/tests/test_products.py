def test_create_product_success(client):
    """Checks if the API returns status 201, correct data, and id and created_at fields."""
    payload = {
        "name": "LaptopDell15",
        "price": 3500.0,
        "category": "Elektronika",
        "quantity": 10,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["category"] == payload["category"]
    assert data["quantity"] == payload["quantity"]
    assert "id" in data
    assert "created_at" in data


def test_create_product_price_below_category_limit(client):
    """Electronics: min 50 PLN limit (20 PLN -> 422)."""
    payload = {
        "name": "CheapMouse",
        "price": 20.0,
        "category": "Elektronika",
        "quantity": 5,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 422


def test_create_product_electronics_price_above_limit(client):
    """Electronics: max 50,000 PLN limit (60,000 PLN -> 422)."""
    payload = {
        "name": "SuperComputer",
        "price": 60000.0,
        "category": "Elektronika",
        "quantity": 1,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 422


def test_create_book_price_limits(client):
    """Books: price limits of 5.0 - 500.0 PLN."""
    res_ok = client.post(
        "/api/v1/products",
        json={"name": "KsiazkaPython", "price": 100.0, "category": "Ksiazka"},
    )
    assert res_ok.status_code == 201

    res_low = client.post(
        "/api/v1/products",
        json={"name": "TaniaKsiazka", "price": 2.0, "category": "Ksiazka"},
    )
    assert res_low.status_code == 422

    res_high = client.post(
        "/api/v1/products",
        json={"name": "DrogaKsiazka", "price": 600.0, "category": "Ksiazka"},
    )
    assert res_high.status_code == 422


def test_create_clothing_price_limits(client):
    """Clothing: price limits of 10.0 - 5,000.0 PLN."""
    res_ok = client.post(
        "/api/v1/products",
        json={"name": "KurtkaZimowa", "price": 450.0, "category": "Odziez"},
    )
    assert res_ok.status_code == 201

    res_low = client.post(
        "/api/v1/products",
        json={"name": "TaniSzalik", "price": 5.0, "category": "Odziez"},
    )
    assert res_low.status_code == 422

    res_high = client.post(
        "/api/v1/products",
        json={"name": "DrogieFutro", "price": 7000.0, "category": "Odziez"},
    )
    assert res_high.status_code == 422


def test_create_product_with_banned_phrase(client):
    """Verifies that creating a product containing a banned phrase returns status 400."""
    client.post("/api/v1/banned-phrases", json={"name": "Dell"})

    payload = {
        "name": "LaptopDell15",
        "price": 3500.0,
        "category": "Elektronika",
        "quantity": 10,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 400
    assert "contains banned phrase" in response.json()["detail"]


def test_name_too_short(client):
    """Verifies that creating a product with a name shorter than the minimum length returns status 422."""
    payload = {"name": "AB", "price": 3500.0, "category": "Elektronika", "quantity": 10}
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 422


def test_name_with_invalid_characters(client):
    """Verifies that creating a product with invalid characters in the name returns status 422."""
    payload = {
        "name": "*()",
        "price": 3500.0,
        "category": "Elektronika",
        "quantity": 10,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 422


def test_duplicate_product_name_fails(client):
    """Verifies that creating a product with an already existing name returns status 400."""
    payload_1 = {
        "name": "DellMonitor",
        "price": 1500.0,
        "category": "Elektronika",
        "quantity": 10,
    }
    response = client.post("/api/v1/products", json=payload_1)
    assert response.status_code == 201

    payload_2 = {
        "name": "DellMonitor",
        "price": 1500.0,
        "category": "Elektronika",
        "quantity": 10,
    }
    response = client.post("/api/v1/products", json=payload_2)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_negative_quantity_fails(client):
    """Verifies that creating a product with a negative quantity returns status 422."""
    payload = {
        "name": "KeyboardRGB",
        "price": 350.0,
        "category": "Elektronika",
        "quantity": -5,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 422


def test_default_quantity_is_zero(client):
    """Verifies that the product quantity defaults to 0 when omitted in the payload."""
    payload = {
        "name": "MouseWireless",
        "price": 120.0,
        "category": "Elektronika",
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 201
    assert response.json()["quantity"] == 0


def test_get_all_products(client):
    """Tests retrieving the list of all products, initially empty and then populated."""
    res_empty = client.get("/api/v1/products")
    assert res_empty.status_code == 200
    assert res_empty.json() == []

    client.post(
        "/api/v1/products",
        json={"name": "Prod1", "price": 100.0, "category": "Elektronika"},
    )
    client.post(
        "/api/v1/products",
        json={"name": "Prod2", "price": 200.0, "category": "Elektronika"},
    )

    res_all = client.get("/api/v1/products")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 2


def test_get_product_by_id(client):
    """Tests retrieving an existing product by its ID."""
    payload = {
        "name": "MonitorUltra",
        "price": 2500.0,
        "category": "Elektronika",
        "quantity": 2,
    }
    create_response = client.post("/api/v1/products", json=payload)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["category"] == payload["category"]
    assert data["quantity"] == payload["quantity"]
    assert data["id"] == product_id
    assert "created_at" in data


def test_get_product_not_found(client):
    """Verifies that retrieving a non-existent product ID returns status 404."""
    response = client.get("/api/v1/products/99999")
    assert response.status_code == 404


def test_update_product_price(client):
    """Tests successfully updating the price of an existing product."""
    create_res = client.post(
        "/api/v1/products",
        json={"name": "SluchawkiBT", "price": 200.0, "category": "Elektronika"},
    )
    product_id = create_res.json()["id"]

    update_res = client.put(f"/api/v1/products/{product_id}", json={"price": 250.0})
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 250.0
    assert update_res.json()["name"] == "SluchawkiBT"


def test_update_product_to_taken_name_fails(client):
    """Verifies that renaming a product to an existing product's name returns status 400."""
    client.post(
        "/api/v1/products",
        json={"name": "ProduktPierwszy", "price": 100.0, "category": "Elektronika"},
    )
    res2 = client.post(
        "/api/v1/products",
        json={"name": "ProduktDrugi", "price": 100.0, "category": "Elektronika"},
    )
    id2 = res2.json()["id"]

    update_res = client.put(f"/api/v1/products/{id2}", json={"name": "ProduktPierwszy"})
    assert update_res.status_code == 400
    assert "already taken" in update_res.json()["detail"]


def test_delete_product(client):
    """Tests deleting a product and verifies it can no longer be retrieved."""
    create_res = client.post(
        "/api/v1/products",
        json={"name": "DoUsuniecia", "price": 100.0, "category": "Elektronika"},
    )
    product_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/products/{product_id}")
    assert del_res.status_code == 200

    get_res = client.get(f"/api/v1/products/{product_id}")
    assert get_res.status_code == 404

def test_save_product_history(client):
    """Tests correct saving history"""
    new_value = 3500.0
    old_value = 3000.0
    payload = {
        "name": "LaptopDell15",
        "price": old_value,
        "category": "Elektronika",
        "quantity": 10,
    }
    create_response = client.post("/api/v1/products", json=payload)
    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    update_res = client.put(f"/api/v1/products/{product_id}", json={"price": new_value})
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 3500.0
    assert update_res.json()["name"] == "LaptopDell15"

    history_res = client.get(f"/api/v1/products/{product_id}/history")
    data = history_res.json()
    assert history_res.status_code == 200
    assert data[0]["id"] == 1
    assert data[0]["id_product"] == product_id
    assert data[0]["variable_name"] == "price"
    assert data[0]["new_value"] == str(new_value)
    assert data[0]["old_value"] == str(old_value)

def test_save_product_history_not_found(client):
    product_id = 99999
    history_res = client.get(f"/api/v1/products/{product_id}/history")
    assert history_res.status_code == 404