from fastapi import FastAPI

from app.routers import patients, doctors, appointments

app = FastAPI(title="Hospital Appointment Management API")

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/")
def root():
    return {"message": "Hospital Appointment Management API is running"}