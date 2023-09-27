import pyqrcode
from fastapi import HTTPException
from models.dbModels import UserModel, Userbankmodel
from models.fastModels import UserBank
from sqlalchemy.orm import Session
from models import engine

db1 = Session(autocommit=False, autoflush=False, bind=engine)


def generateQRCode():
    qrcode = pyqrcode.create("arjun.gadvi@okaxis")
    return qrcode.png("myUPID.png", scale=8)


def create_bank(db: Session, user: str, bank: UserBank):
    bankModel = db.query(Userbankmodel).filter_by(bankname=bank.bankname).first()
    if bankModel:
        raise HTTPException(status_code=404, detail=f"Bank {bank.bankname} exist choose another")
    userbankToDB = Userbankmodel(
        bankname=bank.bankname,
        bankaccnum=bank.bankaccnum,
        bankifsccode=bank.bankifsccode)
    userM = db.query(UserModel).filter_by(username=user).first()
    userbankToDB.user = userM
    db.add(userbankToDB)
    db.commit()
    db.refresh(userbankToDB)
    return {"status": "success"}


def get_banks(db: Session, user: str):
    userModel = db.query(UserModel).filter_by(email=user).first()
    return {
        "number": userModel.number, "name": userModel.firstname + ' ' + userModel.lastname,
        "banks": userModel.banks
    }


def get_bank(db: Session, bid: str):
    bankModel = db.query(Userbankmodel).filter_by(bid=bid).first()
    return bankModel


def update_bank(db: Session, user: str, bank: UserBank):
    return {"status": "success"}


def delete_bank(db: Session, bid: int, username: str):
    bankModel = db.query(Userbankmodel).filter_by(bid=bid).first()
    if bankModel is None:
        raise HTTPException(status_code=404, detail=f"User {bid} does not exist")
    db.query(Userbankmodel).filter_by(bid=bid).delete()
    db.commit()
    return {"status": "success"}
