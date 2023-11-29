from fastapi import HTTPException
from models.dbModels import UserModel, Walletmodel, Txnmodel
from models.fastModels import UserWallet
from components.commonutils import STATUS_CODE, STATUS_COLOR
from sqlalchemy.orm import Session
from models import engine

db1 = Session(autocommit=False, autoflush=False, bind=engine)


def create_wallet(db: Session, email: str, wallet: UserWallet):
    walletModel = db.query(Walletmodel).filter_by(wid=wallet.wid).first()
    if walletModel:
        raise HTTPException(status_code=404, detail=f"Wallet {wallet.wid} exist choose another")
    walletToDB = Walletmodel(walletamt=wallet.walletamt, status=wallet.status)
    userM = db.query(UserModel).filter_by(email=email).first()
    walletToDB.user = userM
    db.add(walletToDB)
    db.commit()
    db.refresh(walletToDB)
    return {"status": "success"}


def get_wallets(db: Session, email: str):
    userModel = db.query(UserModel).filter_by(email=email).first()
    wallets = []
    for wallet in userModel.wallets:
        for txn in wallet.txn:
            wallets.append({ "wid": wallet.wid, "dated": txn.dated, "type": txn.txntype,
                            "walletamt": txn.txnamt,
                            "status": {"code": STATUS_CODE[str(txn.status)].upper(),
                                       "color": STATUS_COLOR[str(txn.status)]}})
    return wallets


def get_wallet(db: Session, wid: str):
    walletModel = db.query(Walletmodel).filter_by(wid=wid).first()
    return walletModel


def update_wallet(db: Session, wid: str):
    return {"status": "success"}


def delete_wallet(db: Session, email: str, wid: int):
    walletModel = db.query(Walletmodel).filter_by(wid=wid).first()
    if walletModel is None:
        raise HTTPException(status_code=404, detail=f"User {wid} does not exist")
    db.query(Walletmodel).filter_by(wid=wid).delete()
    db.commit()
    return {"status": "success"}

def recharge_wallet(db: Session, email: str, amt: str):
    userM = db.query(UserModel).filter_by(email=email).first()

    userM.wallets[0].walletamt = str((int(userM.wallets[0].walletamt)+int(amt)))
    db.commit()

    db.add(Txnmodel(txnamt=amt, txntype="IN", status=0, wallet_id=userM.wallets[0].wid))
    db.commit()

    return {"status": "success", "amt":amt, "walletAmt":userM.wallets[0].walletamt}


def withdraw_wallet(db: Session, email: str, amt: str):
    userM = db.query(UserModel).filter_by(email=email).first()

    userM.wallets[0].walletamt = str((int(userM.wallets[0].walletamt)-int(amt)))
    db.commit()

    db.add(Txnmodel(txnamt=amt, txntype="OUT", status=0, wallet_id=userM.wallets[0].wid))
    db.commit()

    return {"status": "success", "amt":amt, "walletAmt":userM.wallets[0].walletamt}
