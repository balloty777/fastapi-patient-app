# main.py
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, computed_field, field_validator, model_validator,ValidationError
from typing import List, Dict, Optional, Annotated, Literal
import json

app = FastAPI()

# -----------------------------
# Utility Functions
# -----------------------------
def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

# -----------------------------
# Pydantic Models
# -----------------------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Patient ID', examples=['P001'])]
    name: Annotated[str, Field(..., max_length=50, description='Patient Name')]
    city: Annotated[str, Field(..., description='City')]
    age: Annotated[int, Field(...,gt=0, le=110, description='Age')]
    gender: Annotated[Literal[...,'Male', 'Female', 'Others'], Field(...)]
    height: Annotated[float, Field(...,gt=0, description='Height in meters')]
    weight: Annotated[float, Field(...,gt=0, description='Weight in kg')]
    email: Annotated[EmailStr,Field(...,description='Email of the Patient')]
    married: Annotated[bool,Field(...,description='Married status of patient in True or False')]
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, value):
        if value.split('@')[-1] not in ['hdfc.com', 'icici.com']:
            raise ValueError('Email domain must be hdfc.com or icici.com')
        return value

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Emergency contact required for patients over 60')
        return model

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.calculate_bmi
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['Male', 'Female', 'Others','male','female','others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

# -----------------------------
# Routes
# -----------------------------
@app.get('/patients')
def view_all():
    return load_data()

@app.get('/patients/{patient_id}')
def view_patient(patient_id: str = Path(..., description='Patient ID')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/patients/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort by height, weight, or bmi'),
    order: str = Query('asc', description='asc or desc')
):
    data = load_data()
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid sort field. Choose from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Order must be "asc" or "desc"')

    sort_reverse = order == 'desc'
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by) or round(x['weight'] / (x['height'] ** 2), 2),
        reverse=sort_reverse
    )
    return sorted_data

@app.post('/patients')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put('/patients/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    existing = data[patient_id]
    updates = patient_update.model_dump(exclude_unset=True)
    existing.update(updates)
    try:
        patient_obj = Patient(id=patient_id, **existing)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    data[patient_id] = patient_obj.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'messege':'Patient deleted successfully'})