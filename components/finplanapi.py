from fastapi import HTTPException
from models.dbModels import UserModel, Financeplanmodel
from models.fastModels import FinPlan
from sqlalchemy.orm import Session
from models import engine

db1 = Session(autocommit=False, autoflush=False, bind=engine)


def create_finplan(db: Session, finplan: FinPlan):
    finplanModel = db.query(Financeplanmodel).filter_by(planname=finplan.planname).first()
    if finplanModel:
        raise HTTPException(status_code=404, detail=f"Finance Plan {finplan.planname} exist choose another")
    finplanModelToDB = Financeplanmodel(
        planname=finplan.planname,
        price=finplan.price,
        dailyincome=finplan.dailyincome,
        days=finplan.days)
    #userM = db.query(UserModel).filter_by(username=user).first()
    #finplanModelToDB.user = userM
    db.add(finplanModelToDB)
    db.commit()
    db.refresh(finplanModelToDB)
    return {"status": "success"}


def get_finplan(db: Session, status: str):
    finplan = db.query(Financeplanmodel).filter_by(status=status).all()
    return finplan


def update_finplan(db: Session, user: str, bank: FinPlan):
    return {"status": "success"}


def delete_finplan(db: Session, username: str, fid: int):
    finModel = db.query(Financeplanmodel).filter_by(fid=fid).first()
    if finModel is None:
        raise HTTPException(status_code=404, detail=f"Finance Plan ID:{fid} does not exist")
    db.query(Financeplanmodel).filter_by(fid=fid).delete()
    db.commit()
    return {"status": "success"}
