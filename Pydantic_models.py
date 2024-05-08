from typing import Optional
from pydantic import BaseModel

class PatientUpdate(BaseModel):
    identifier: str
    name: Optional[str]
    gender: Optional[str]
    birthDate: Optional[str]
    deceased: Optional[str]
    address: Optional[str]