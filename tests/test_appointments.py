def _create_patient(client):
    response = client.post(
        "/patients/",
        json={"name": "Test Patient", "email": "patient@example.com", "phone": "5555555555"},
    )
    return response.json()["id"]


def _create_doctor(client):
    response = client.post(
        "/doctors/",
        json={"name": "Dr. Test", "specialization": "General"},
    )
    return response.json()["id"]


def test_create_appointment_success(client):
    patient_id = _create_patient(client)
    doctor_id = _create_doctor(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id


def test_get_appointments(client):
    patient_id = _create_patient(client)
    doctor_id = _create_doctor(client)

    client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T09:00:00",
            "appointment_end": "2026-08-15T10:00:00",
        },
    )
    response = client.get("/appointments/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_appointment_by_id(client):
    patient_id = _create_patient(client)
    doctor_id = _create_doctor(client)

    create_response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T14:00:00",
            "appointment_end": "2026-08-15T15:00:00",
        },
    )
    appointment_id = create_response.json()["id"]

    response = client.get(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    assert response.json()["patient_id"] == patient_id


def test_get_appointment_not_found(client):
    response = client.get("/appointments/999")
    assert response.status_code == 404


def test_reject_overlapping_appointment(client):
    patient_id = _create_patient(client)
    doctor_id = _create_doctor(client)

    client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T10:30:00",
            "appointment_end": "2026-08-15T11:30:00",
        },
    )
    assert response.status_code == 400
    assert "overlapping" in response.json()["detail"].lower()


def test_allow_non_overlapping_appointment(client):
    patient_id = _create_patient(client)
    doctor_id = _create_doctor(client)

    client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T11:00:00",
            "appointment_end": "2026-08-15T12:00:00",
        },
    )
    assert response.status_code == 201


def test_create_appointment_invalid_patient(client):
    doctor_id = _create_doctor(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": 999,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )
    assert response.status_code == 404


def test_create_appointment_invalid_doctor(client):
    patient_id = _create_patient(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": 999,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )
    assert response.status_code == 404


def test_create_appointment_invalid_time_range(client):
    patient_id = _create_patient(client)
    doctor_id = _create_doctor(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-15T11:00:00",
            "appointment_end": "2026-08-15T10:00:00",
        },
    )
    assert response.status_code == 400