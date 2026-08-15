from datetime import datetime

from pydantic import BaseModel


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        from_attributes = True
