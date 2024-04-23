from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ORMs import Patient
from Database_Connection import get_db_connection_string

app = FastAPI()

conn_str = get_db_connection_string()
engine = create_engine(conn_str)

@app.get("/patients")
def read_patients():
    with Session(engine) as session:
        patients = session.query(Patient).all()
        return {"patients": [patient.__dict__ for patient in patients]}