import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class NewBook(BaseModel):
    title: str
    author : str

    
books = [
    {
        "id": 1,
        "title": "book1",
        "author": "author1",
    },
    {
        "id": 2,
        "title": "book2",
        "author": "author2",
    },
]


@app.get("/books", tags=["Книги"], summary="Получить все книги")
def read_books():
    return books


@app.get("/books/{id}", tags=["Книги"], summary="Получить книгу по id")
def read_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.post('/books/')
def create_book(new_book: NewBook):
    books.append(
        {
            'id': len(books) + 1,
            'title': new_book.title,
            'author' : new_book.author
        }
    )
    return {'success': True}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
