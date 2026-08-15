from pydantic import BaseModel


class DoctorBase(BaseModel):
    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: int

    class Config:
        from_attributes = True
