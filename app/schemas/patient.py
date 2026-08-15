from pydantic import BaseModel, EmailStr


class PatientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    id: int

    class Config:
        from_attributes = True