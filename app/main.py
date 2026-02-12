from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Task Manager")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()
