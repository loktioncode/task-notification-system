from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...crud import notification as crud_notification
from ...schemas.notification import Notification
from ...database import get_db
from ...api.deps import get_current_user
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[Notification])
def get_notifications(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    notifications = crud_notification.get_user_notifications(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return notifications

@router.post("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = crud_notification.mark_as_read(
        db=db, notification_id=notification_id, user_id=current_user.id
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "success"}