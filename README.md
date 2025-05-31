# FastAPI Patient App

This is a FastAPI application to manage patient records. It includes features like data validation, BMI calculation, and sorting.

---

## Features

- Add, view, and update patient records
- Validate email domains and emergency contacts
- Automatically calculate BMI and provide health verdict
- Sort patients by height, weight, or BMI

---

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/balloty777/fastapi-patient-app.git
   cd fastapi-patient-app
2. Create and activate a virtual environment (optional but recommended):
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3. Install dependencies:
pip install -r requirements.txt
Usage
Run the app locally:
uvicorn main:app --reload
Open your browser and visit:
http://127.0.0.1:8000/docs
to explore the API with interactive Swagger UI.

API Endpoints
Method	Endpoint	Description
GET	/patients	Get all patients
GET	/patients/{id}	Get patient by ID
GET	/patients/sort	Sort patients by height, weight, or BMI
POST	/patients	Create a new patient
PUT	/patients/{id}	Update an existing patient

Notes
Patient data is stored in patients.json file.

Emails must be from hdfc.com or icici.com.

Patients over 60 must have an emergency contact listed.

Author
Ayush Pandey

License
This project is licensed under the MIT License.
