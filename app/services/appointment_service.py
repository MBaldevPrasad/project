from sqlalchemy.orm import Session

from app.models.appointment import Appointment


def has_overlapping_appointment(db: Session, doctor_id: int, new_start, new_end) -> bool:
    overlapping = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_start < new_end,
            Appointment.appointment_end > new_start,
        )
        .first()
    )
    return overlapping is not None
