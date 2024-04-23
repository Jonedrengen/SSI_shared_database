from sqlalchemy import Column, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = "Patient"
    __table_args__ = {"schema": "dbo"}

    identifier = Column("identifier", VARCHAR(255), primary_key=True)
    name = Column("name", VARCHAR(255))
    gender = Column("gender", VARCHAR(255))
    birthDate = Column("birthDate", VARCHAR(255))
    deceased = Column("deceased", VARCHAR(255))
    address = Column("address", VARCHAR(255))

    def __init__(self, identifier, name, gender, birthDate, deceased, address):
        self.identifier = identifier
        self.name = name
        self.gender = gender
        self.birthDate = birthDate
        self.deceased = deceased
        self.address = address

    def __repr__(self):
        return f"{self.identifier}, {self.name}, {self.gender}, {self.birthDate}, {self.deceased}, {self.address}"