from fastapi import FastAPI, Path, HTTPException, Query
import json
from model import Book

app = FastAPI()

def load_data():
    with open('Books.json', 'r') as f: 
        data = json.load(f)
    return data


@app.get('/')
async def hello():
    return {"message": "Library Management API"}


@app.get('/about')
async def about(): 
    return {'message': 'A functioning API for books'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/library/{book_id}')
def view_book_by_id(book_id: str = Path(..., description='Id of the book', example='P100')):
    data = load_data()  

    for book in data:
        if book.get("book_id") == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

     
def save_books(data):
    with open('Books.json', "w") as f:
        json.dump(data, f, indent=4)


@app.get('/sort')
def sort_book(sort_by: str = Query(..., description = 'The way you want the data to be sorted', 
example = 'By Name or Author or Pages or Price'), order: str = Query('asc', description = 'Sort in ascending order')):
    valid_fields = ['name', 'author', 'year']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f'Invalid field selected from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = f'Invalid, select either asc or desc')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data, key = lambda x: x.get(sort_by, 0), reverse = sort_order)

    return sorted_data


@app.post("/library")
async def add_book(new_book: Book):
    data = load_data()  
    
    # Checking for duplicate ID
    for existing_book in data:
        if existing_book.get("book_id") == new_book.book_id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")

    
    # Appending the new book
    data.append({
        "book_id": new_book.book_id,
        "name": new_book.name,
        "author": new_book.author,
        "year": new_book.year,
        "pages": new_book.pages,
        "price": new_book.price
    })
    
    save_books(data)
    return {"message": "Book added successfully", "book": new_book}

@app.delete("/library")
async def delete_book(deleted_book: Book):
    data = load_data()

    # Finding the book to delete
    book_to_delete = None
    for book in data:
        if book.get("book_id") == deleted_book.book_id:
            book_to_delete = book
            break

    if not book_to_delete:
        raise HTTPException(status_code=404, detail="Book with this ID does not exist")

    # Removing the book from the list
    data.remove(book_to_delete)

    # Saving the updated data
    save_books(data)

    return {"message": "Book deleted successfully", "book": deleted_book}

@app.put("/library")
async def update_book(updated_book: Book):
    data = load_data()
    book_to_update = None
    for book in data:
        if book.get("book_id") == updated_book.book_id:
            book_to_update = book
            break

    if not book_to_update:
        raise HTTPException(status_code=404, detail="Book with this ID does not exist")

   

    book_to_update["name"] = updated_book.name
    book_to_update["author"] = updated_book.author
    book_to_update["year"] = updated_book.year
    book_to_update["pages"] = updated_book.pages
    book_to_update["price"] = updated_book.price

    

    save_books(data)
    return {"message": "Book updated successfully", "book": updated_book}