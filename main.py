from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student CRUD API")


@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


@app.get("/students/", response_model=list[schemas.Student])
def get_all_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
):
    updated_student = crud.update_student(db, student_id, student)

    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db, student_id)

    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}