from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f: 
        data = await json.load(f)
    return data


@app.get('/')
async def hello():
    return {"message": "Patient Management API"}


@app.get('/about')
async def about():
    return {'message': 'A functioning API for patients'}

@app.get('/view')
async def view():
    data = await load_data()
    return data

@app.get('/patient/{patient_id}')
async def view_patient(patient_id: str = Path(..., description = 'Id of the patient', example = 'P009')):
    #loading all the patients 
    data = await load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = 'Patient not found') 
     
@app.get('/sort')
async def sort_patients(sort_by: str = Query(..., description = 'The way you want the data to be sorted', 
example = 'By height or weight'), order: str = Query('asc', description = 'Sort in ascending order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f'Invalid field selected from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = f'Invalid, select either asc or desc')

    data = await load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)

    return sorted_data