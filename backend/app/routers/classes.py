from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..auth import get_current_active_user, get_admin_user
from .. import crud, schemas, models

router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("/", response_model=List[schemas.ClassWithDetails])
def get_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Get all classes (admin only)"""
    classes = crud.get_classes(db, skip=skip, limit=limit)
    return classes


@router.get("/{class_id}", response_model=schemas.ClassWithDetails)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Get a specific class (admin only)"""
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada"
        )
    return db_class


@router.post("/", response_model=schemas.Class)
def create_class(
    class_data: schemas.ClassCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new class (admin only)"""
    # Verify that the room exists
    room = crud.get_room(db, room_id=class_data.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada"
        )
    
    # Verify that end time is after start time
    if class_data.end_time <= class_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Horário de término deve ser posterior ao horário de início"
        )
    
    # Create the class
    db_class = crud.create_class(db=db, class_data=class_data)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflito de horário: já existe uma aula ou agendamento neste período"
        )
    
    return db_class


@router.put("/{class_id}", response_model=schemas.Class)
def update_class(
    class_id: int,
    class_update: schemas.ClassUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a class (admin only)"""
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada"
        )
    
    updated_class = crud.update_class(db=db, class_id=class_id, class_update=class_update)
    return updated_class


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a class (admin only)"""
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada"
        )
    
    success = crud.delete_class(db=db, class_id=class_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar aula"
        )
    
    return {"message": "Aula deletada com sucesso"}


@router.get("/room/{room_id}", response_model=List[schemas.Class])
def get_classes_by_room(
    room_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get classes for a specific room"""
    room = crud.get_room(db, room_id=room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada"
        )
    
    classes = crud.get_classes_by_room(
        db, room_id=room_id, start_date=start_date, end_date=end_date
    )
    return classes
