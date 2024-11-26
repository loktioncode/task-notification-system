from typing import List
from sqlalchemy.orm import Session
from ..models.notification import Notification
from ..schemas.notification import NotificationCreate
from .base import CRUDBase

class CRUDNotification(CRUDBase):
    def get_user_notifications(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_notification(
        self, db: Session, *, obj_in: NotificationCreate
    ) -> Notification:
        db_obj = Notification(
            type=obj_in.type,
            message=obj_in.message,
            user_id=obj_in.user_id,
            task_id=obj_in.task_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def mark_as_read(
        self, db: Session, *, notification_id: int, user_id: int
    ) -> Notification:
        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
            .first()
        )
        if notification:
            notification.is_read = True
            db.add(notification)
            db.commit()
            db.refresh(notification)
        return notification

notification = CRUDNotification(Notification)