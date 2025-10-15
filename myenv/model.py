from pydantic import BaseModel

class Book(BaseModel):
    book_id: str       
    name: str
    author: str
    year: int
    pages: int
    price: float
