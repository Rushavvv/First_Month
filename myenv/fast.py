from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f: 
        data = json.load(f)
    return data


@app.get('/')
async def hello():
    return {"message": "Patient Management API"}


@app.get('/about')
async def about():
    return {'message': 'A functioning API for patients'}

@app.get('/view')
async def view():
    data = load_data()
    return data