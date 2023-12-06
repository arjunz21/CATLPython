from fastapi import HTTPException
from models.dbModels import UserModel, Financeplanmodel, Txnmodel
from models.fastModels import FinPlan
from sqlalchemy.orm import Session
from models import engine

db1 = Session(autocommit=False, autoflush=False, bind=engine)


def create_user_finteam(db: Session, email: str, finplan: str):
    userM = db.query(UserModel).filter_by(email=email).first()
    if not userM:
        raise HTTPException(status_code=404, detail=f"User {email} does not exist")
    finplanModel = db.query(Financeplanmodel).filter_by(planname=finplan).first()
    if not finplanModel:
        raise HTTPException(status_code=404, detail=f"Finance Plan {finplan} does not  exist")
    
    if (int(userM.wallets[0].walletamt)) < 0 or (int(userM.wallets[0].walletamt) < int(finplanModel.price)):
        raise HTTPException(status_code=404, detail=f"Insufficient Wallet Amount {userM.wallets[0].walletamt}, Please Recharge...")
    else:
        userM.wallets[0].walletamt = str((int(userM.wallets[0].walletamt)-int(finplanModel.price))*0.09)
        db.commit()

        db.add(Txnmodel(txnamt=finplanModel.price, txntype="OUT", status=7, wallet_id=userM.wallets[0].wid))
        db.commit()
        
        userM.finplans.append(finplanModel)
        db.commit()
        db.refresh(userM)
    return {"status": "success"}


def get_user_finteam(db: Session, email: str):
    user = db.query(UserModel).filter_by(email=email).first()
    fints = []
    for fin in user.finplans:
        finPlan = db.query(Financeplanmodel).filter_by(planname=fin.planname).first()
        for member in finPlan.members:
            if user.refcode == member.invitecode:
                fints.append(
                    {"plan": fin.planname, "number": member.number, "email": member.email,
                    "name": member.firstname + ' ' + member.lastname, "level": "1", "dated": "03-06 21:53"})
    return fints


def get_user_finplan(db: Session, email: str):
    finplans = db.query(UserModel).filter_by(email=email).first().finplans
    return finplans


def update_user_finteam(db: Session, email: str, bank: FinPlan):
    return {"status": "success"}


def delete_user_finteam(db: Session, email: str, fid: str):
    userM = db.query(UserModel).filter_by(email=email).first()
    if not userM:
        raise HTTPException(status_code=404, detail=f"User {email} does not  exist")
    finplanModel = db.query(Financeplanmodel).filter_by(fid=fid).first()
    if not finplanModel:
        raise HTTPException(status_code=404, detail=f"Finance Plan {fid} does not  exist")
    userM.finplans.remove(finplanModel)
    db.commit()
    return {"status": "success"}
