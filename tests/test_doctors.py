def test_create_doctor(client):
    response = client.post(
        "/doctors/",
        json={"name": "Dr. Smith", "specialization": "Cardiology"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dr. Smith"
    assert data["specialization"] == "Cardiology"
    assert "id" in data


def test_get_doctors(client):
    client.post(
        "/doctors/",
        json={"name": "Dr. Lee", "specialization": "Neurology"},
    )
    response = client.get("/doctors/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_doctor_by_id(client):
    create_response = client.post(
        "/doctors/",
        json={"name": "Dr. Patel", "specialization": "Dermatology"},
    )
    doctor_id = create_response.json()["id"]

    response = client.get(f"/doctors/{doctor_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Dr. Patel"


def test_get_doctor_not_found(client):
    response = client.get("/doctors/999")
    assert response.status_code == 404