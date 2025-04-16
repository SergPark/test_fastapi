from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from pydantic import BaseModel, Field, EmailStr, ConfigDict

engine = create_engine("sqlite:///books.db")
new_session = Session(engine)

app = FastAPI()


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BookAddSchema):
    id: int


@app.post("/update_metadata")
def update_metadata():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {"ok": True}


@app.post("/books")
def add_book(data: BookAddSchema):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    new_session.add(new_book)
    new_session.commit()
    return {"ok": True}


@app.get("/books")
def get_books():
    query = select(BookModel)
    data = new_session.execute(query)
    # check_res = data
    # print(check_res)
    return data.scalars().all()
