#Use their official sources
from fastapi import FastAPI, HTTPException
#Pydantic is used for data validation
from pydantic import BaseModel

description = """
Health-Dashboard API is a simple service, to request patients records and create new patient record.

##HTTP REQUESTS
You can use a POST and GET meaning you can 
**Create new patient record**
**Read each patient record by ID**
"""
#Create the HTTP connection point
app = FastAPI(
    title ="Health-Dashboard API",
    Summary="API for managing patient health records",
    version = "0.1.0",
    contact={"name":"David Anthony"},
)

#Use the BaseModel and define the patient blueprint
class PatientInfo(BaseModel):
    name: str
    age: int
    sex: str
    nhs_number: str
    email_address: str
    condition: str

#For a quick demonstration - Patients database (create an id field with "id")
# Using keys as strings and values as their type in a dictionary, you can nest {} inside:   {1 :{}} or {1 : ..}

patients_db = {
    1 : {"id": 1, "name": "David Anthony", "age": 22, "sex":"male", "nhs_number": "1324515", "email_address":"david@gmail.com", "condition":"Currently experiencing a cold and an abnormally high temperature" },
    2 : {"id": 2, "name": "Lana felino", "age": 29, "sex":"female", "nhs_number": "5316165", "email_address":"lana@gmail.com", "condition":"Suffered a minor leg injury at 9:23am" },
}

# Next id builds on previous
next_id = 3

#Create getter method
@app.get("/api/patients")
def my_list_patients():
    # Use a doc string with """ """ and put what it does. Also use the list() method and .values() top connect with patients_db for the dictionary.
    """Retrieve all patients"""
    return list(patients_db.values())

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: int):
    """Retrieve a single patient"""
    # If coondition to check if a patient does not exist inside the database to throw exception
    if patient_id not in patients_db:
        # Raise exception for patient)id not found using 404.
        raise HTTPException(status_code = 404, detail="Patient not found")
    # Return the database as a key []. So embedd it inside the function
    return patients_db[patient_id]


# Call pydantic method name defined to use
@app.post("/api/patients", status_code = 201)
def create_patient(patient: PatientInfo):
# Use global for the next_id to make it persist throughout code
    global next_id
    # Define new patient variable, then convert the Pydantic model into a dictionary with model_dump()
    new_patient = {"id": next_id, **patient.model_dump()}
    patients_db[next_id] = new_patient
    # Increment next_id
    next_id = next_id + 1
    # return new patient
    return new_patient

@app.get("/")
def get_root_address():
    return {"message":"Welcome to the Patient and Health Dashboard API"}


