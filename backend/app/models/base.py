from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Any

Base = declarative_base()

class CRUDBase:
    def __init__(self, model: Any):
        self.model = model

    def get(self, db: Session, id: Any):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Any) -> Any:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj