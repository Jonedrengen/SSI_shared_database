from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORMs import Patient, Base
from Database_Connection import get_db_connection_string

# replace with your actual database connection string
DATABASE_URL = get_db_connection_string()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a new session
db = SessionLocal()

# create a new patient
new_patient = Patient(
    identifier="123",
    name="Test Patient",
    gender="male",
    birthDate="2000-01-01",
    deceased="no",
    address="123 Test St",
)

# add the new patient to the session
db.add(new_patient)

# commit the session
db.commit()

# query the database for the patient we just added
patient = db.query(Patient).filter(Patient.identifier == "123").first()

# print the patient
print(patient)