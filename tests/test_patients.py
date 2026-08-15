def test_create_patient(client):
    response = client.post(
        "/patients/",
        json={"name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


def test_get_patients(client):
    client.post(
        "/patients/",
        json={"name": "Jane Doe", "email": "jane@example.com", "phone": "9876543210"},
    )
    response = client.get("/patients/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_patient_by_id(client):
    create_response = client.post(
        "/patients/",
        json={"name": "Alice", "email": "alice@example.com", "phone": "1112223333"},
    )
    patient_id = create_response.json()["id"]

    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_patient_not_found(client):
    response = client.get("/patients/999")
    assert response.status_code == 404