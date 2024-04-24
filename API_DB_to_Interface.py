import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from ORMs import Patient
from Database_Connection import get_db_connection_string

app = FastAPI()

conn_str = get_db_connection_string()
engine = create_engine(conn_str)




# get full patient table
@app.get("/Patient")
def read_patients():
    try:
        with Session(engine) as session:
            patients = session.query(Patient).all()
            return {"patients": [patient.__dict__ for patient in patients]}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, port=8888, host="0.0.0.0")