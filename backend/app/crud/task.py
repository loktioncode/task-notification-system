from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from .base import CRUDBase

class CRUDTask(CRUDBase):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(Task)
            .filter(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_assignee(
        self, db: Session, *, assigned_to_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(Task)
            .filter(Task.assigned_to_id == assigned_to_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: TaskCreate, owner_id: int
    ) -> Task:
        obj_in_data = obj_in.dict()
        db_obj = Task(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(
        self, db: Session, *, db_obj: Task, status: str
    ) -> Task:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

task = CRUDTask(Task)