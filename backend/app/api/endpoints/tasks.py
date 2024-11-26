from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import redis.asyncio as redis

from ...core.config import settings
from ...crud import task as crud_task
from ...crud import notification as crud_notification
from ...schemas.task import Task, TaskCreate, TaskUpdate, TaskStatusUpdate
from ...schemas.notification import NotificationCreate
from ...database import get_db
from ...api.deps import get_current_user
from ...models.user import User

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

@router.post("/", response_model=Task)
async def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    task = crud_task.create_with_owner(
        db=db, obj_in=task_in, owner_id=current_user.id
    )
    
    if task.assigned_to_id:
        # Create notification for assigned user
        notification = NotificationCreate(
            type="task_assigned",
            message=f"You have been assigned a new task: {task.title}",
            user_id=task.assigned_to_id,
            task_id=task.id
        )
        db_notification = crud_notification.create_notification(db=db, obj_in=notification)
        
        # Send real-time notification via Redis
        await redis_client.publish(
            f"user:{task.assigned_to_id}:notifications",
            db_notification.message
        )
    
    return task

@router.get("/", response_model=List[Task])
def get_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    tasks = crud_task.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return tasks

@router.get("/assigned", response_model=List[Task])
def get_assigned_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    tasks = crud_task.get_multi_by_assignee(
        db=db, assigned_to_id=current_user.id, skip=skip, limit=limit
    )
    return tasks

@router.put("/{task_id}/status", response_model=Task)
async def update_task_status(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    status_update: TaskStatusUpdate,
    current_user: User = Depends(get_current_user)
):
    task = crud_task.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    task = crud_task.update_status(db=db, db_obj=task, status=status_update.status)
    
    # Create notification for task owner if updated by assignee
    if task.owner_id != current_user.id:
        notification = NotificationCreate(
            type="task_updated",
            message=f"Task '{task.title}' status updated to: {status_update.status}",
            user_id=task.owner_id,
            task_id=task.id
        )
        db_notification = crud_notification.create_notification(db=db, obj_in=notification)
        
        # Send real-time notification via Redis
        await redis_client.publish(
            f"user:{task.owner_id}:notifications",
            db_notification.message
        )
    
    return task