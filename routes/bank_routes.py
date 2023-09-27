from fastapi import APIRouter

from components import authenticapi, bankapi
from routes import Session, Depends
from routes import UserBank, UserInDB, models

bank_router = APIRouter(
    prefix='/api/bank',
    tags=['User Bank']
)


# UserBankModel Start
@bank_router.put("/register/", response_model=UserBank)
async def create_user_bank(bank: UserBank, db: Session = Depends(models.getdb),
                           current_user: str = Depends(authenticapi.get_current_active_user)):
    bankapi.create_bank(db, current_user, bank)
    return bank


@bank_router.get("/")
def get_user_banks(db: Session = Depends(models.getdb),
                    current_user: str = Depends(authenticapi.get_current_active_user)):
    return bankapi.get_banks(db, current_user)


@bank_router.get("/{bank_id}")
def get_user_bank(bank_id: str, db: Session = Depends(models.getdb),
                     current_user: str = Depends(authenticapi.get_current_active_user)):
    return bankapi.get_bank(db, bank_id)


@bank_router.patch("/{bank_id}")
def update_user_bank(bank: UserBank, db: Session = Depends(models.getdb),
                     current_user: str = Depends(authenticapi.get_current_active_user)):
    return UserInDB


@bank_router.delete("/{bank_id}")
def delete_user_bank(bank_id: int, db: Session = Depends(models.getdb),
                     current_user: str = Depends(authenticapi.get_current_active_user)):
    return bankapi.delete_bank(db, bank_id, current_user)

# UserBankModel End
