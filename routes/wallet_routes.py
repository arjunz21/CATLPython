from fastapi import APIRouter

from components import authenticapi, walletapi
from routes import Session, Depends, models
from routes import UserWallet, User, UserInDB

wallet_router = APIRouter(
    prefix='/api/wallet',
    tags=['User Wallet']
)


# WalletModel Start
@wallet_router.put("/register/", response_model=UserWallet)
async def create_user_wallet(wallet: UserWallet, db: Session = Depends(models.getdb),
                             current_user: str = Depends(authenticapi.get_current_active_user)):
    walletapi.create_wallet(db, current_user, wallet)
    return wallet


@wallet_router.get("/")
def get_user_wallets(db: Session = Depends(models.getdb),
                     current_user: str = Depends(authenticapi.get_current_active_user)):
    return walletapi.get_wallets(db, current_user)


@wallet_router.get("/{wallet_id}")
def get_user_wallet(wallet_id, db: Session = Depends(models.getdb),
                    current_user: str = Depends(authenticapi.get_current_active_user)):
    return walletapi.get_wallet(db, wallet_id)


@wallet_router.patch("/{wallet_id}")
def update_user_wallet(current_user: str = Depends(authenticapi.get_current_active_user)):
    return UserInDB


@wallet_router.delete("/{wallet_id}")
def delete_user_wallet(wid: int, db: Session = Depends(models.getdb),
                       current_user: str = Depends(authenticapi.get_current_active_user)):
    return walletapi.delete_wallet(db, current_user, wid)

# WalletModel End
