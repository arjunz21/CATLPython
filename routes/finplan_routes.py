from fastapi import APIRouter

from components import authenticapi, finplanapi
from routes import Session, Depends, models
from routes import UserInDB, FinPlan

finplan_router = APIRouter(
    prefix='/api/finplan',
    tags=['Finance Plan']
)


# FinancePlanModel Start
@finplan_router.get("/")
async def get_finplan(status: str, db: Session = Depends(models.getdb)):
    finplan = finplanapi.get_finplan(db, status)
    return finplan


@finplan_router.put("/register/", response_model=FinPlan)
async def create_finplan(finplan: FinPlan, db: Session = Depends(models.getdb),
                         current_user: str = Depends(authenticapi.get_current_active_user)):
    finplanapi.create_finplan(db, finplan)
    return finplan


@finplan_router.patch("/{finplan_id}")
def update_finplan(current_user: str = Depends(authenticapi.get_current_active_user)):
    return UserInDB


@finplan_router.delete("/{finplan_id}")
def delete_finplan(fid: int, db: Session = Depends(models.getdb),
                   current_user: str = Depends(authenticapi.get_current_active_user)):
    return finplanapi.delete_finplan(db, current_user, fid)

# FinancePlanModel End
