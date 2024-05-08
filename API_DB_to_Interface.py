import uvicorn
from fastapi import FastAPI, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from ORMs import Patient
from Pydantic_models import PatientUpdate
from Database_Connection import get_db_connection_string
from typing import List

app = FastAPI()

conn_str = get_db_connection_string()
engine = create_engine(conn_str)


@app.get("/Patient", response_model=List[PatientUpdate])
def read_patients():
    try:
        with Session(engine) as session:
            patients = session.query(Patient).all()
            return patients  #FastAPI will automatically convert the SQLAlchemy models to Pydantic models
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.put("/Patient/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate = Body(...)):
    try:
        with Session(engine) as session:
            patient = session.query(Patient).filter(Patient.identifier == patient_id).first()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
            
            for key, value in patient_update.model_dump().items():
                setattr(patient, key, value)
            
            session.commit()
            return {"message": "Patient updated successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run(app, port=8888, host="0.0.0.0")