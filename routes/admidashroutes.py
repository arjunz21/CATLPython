from fastapi import APIRouter

from components import authenticapi, admindashapi
from routes import Session, Depends, models
from routes import UserWallet, User, UserInDB

admindash_router = APIRouter(
    prefix='/api/admindash',
    tags=['Admin Dashboard']
)

#Depends(authenticapi.get_current_active_user)
@admindash_router.get("/")
def get_users_details(db: Session = Depends(models.getdb),
                     current_user: str = "admin@a.com"):
    return admindashapi.get_users_details(db, current_user)