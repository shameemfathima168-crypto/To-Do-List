from contextlib import asynccontextmanager
from datetime import datetime
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
from models import Todo


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="To-Do API", version="1.0.0", lifespan=lifespan)


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    completed: bool | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime
    model_config = {"from_attributes": True}


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/todos", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.completed, Todo.created_at.desc()).all()


@app.post("/api/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    item = Todo(title=payload.title.strip())
    if not item.title:
        raise HTTPException(422, "A task title is required.")
    db.add(item); db.commit(); db.refresh(item)
    return item


@app.patch("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    item = db.get(Todo, todo_id)
    if not item:
        raise HTTPException(404, "Task not found.")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value.strip() if key == "title" else value)
    db.commit(); db.refresh(item)
    return item


@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    item = db.get(Todo, todo_id)
    if not item:
        raise HTTPException(404, "Task not found.")
    db.delete(item); db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
