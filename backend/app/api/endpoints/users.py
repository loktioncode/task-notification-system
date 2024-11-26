from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...crud import user as crud_user
from ...schemas.user import User
from ...database import get_db
from ...api.deps import get_current_user
from ...models.user import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[User])
def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Retrieve all users.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users