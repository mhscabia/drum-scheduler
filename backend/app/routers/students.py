from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.StudentWithDetails])
def read_students(
    skip: int = 0,
    limit: int = 100,    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Get all students (admin only)"""
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@router.post("/", response_model=schemas.Student)
def create_student(
    student: schemas.StudentCreate,    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Create a new student (admin only)"""
    return crud.create_student(db=db, student=student)


@router.get("/{student_id}", response_model=schemas.StudentWithDetails)
def read_student(
    student_id: int,    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Get a specific student (admin only)"""
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado"
        )
    return db_student


@router.put("/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Update a student (admin only)"""
    db_student = crud.update_student(
        db,
        student_id=student_id,
        student_update=student_update
    )
    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado"
        )
    return db_student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Delete a student (admin only)"""
    success = crud.delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado"
        )
    return {"message": "Estudante excluído com sucesso"}


@router.get("/room/{room_id}", response_model=List[schemas.StudentWithDetails])
def read_students_by_room(
    room_id: int,    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    """Get students for a specific room (admin only)"""
    return crud.get_students_by_room(db, room_id=room_id)
