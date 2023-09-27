from routes import Session, Depends, models
from routes import UserInDB, UserFinTeamModel
from fastapi import APIRouter
from components import authenticapi, userfinteamapi


userfinteam_router = APIRouter(
    prefix='/api/userfinteam',
    tags=['User Finance Team']
)


# UserFinanceTeamModel Start
@userfinteam_router.get("/register/")
async def create_user_finteam(finplan: str, db: Session = Depends(models.getdb),
                              current_user: str = Depends(authenticapi.get_current_active_user)):
    return userfinteamapi.create_user_finteam(db, current_user, finplan)


@userfinteam_router.get("/")
async def get_user_finteam(db: Session = Depends(models.getdb),
                           current_user: str = Depends(authenticapi.get_current_active_user)):
    return userfinteamapi.get_user_finteam(db, current_user)


@userfinteam_router.get("/user")
async def get_user_finplan(db: Session = Depends(models.getdb),
                      current_user: str = Depends(authenticapi.get_current_active_user)):
    finplan = userfinteamapi.get_user_finplan(db, current_user)
    return finplan


@userfinteam_router.patch("/{finplan_id}")
def update_user_finteam(current_user: str = Depends(authenticapi.get_current_active_user)):
    return UserInDB


@userfinteam_router.delete("/{fid}")
def delete_user_finteam(fid: str, db: Session = Depends(models.getdb),
                        current_user: str = Depends(authenticapi.get_current_active_user)):
    return userfinteamapi.delete_user_finteam(db, current_user, fid)

# UserFinanceTeamModel End
