from fastapi import HTTPException
from models.dbModels import UserModel
from components.commonutils import STATUS_CODE, STATUS_COLOR
from sqlalchemy.orm import Session
from models import engine

db1 = Session(autocommit=False, autoflush=False, bind=engine)

def get_users_details(db: Session, email: str):
    userModel = db.query(UserModel).all()
    totAmt = 0
    dailyAmt = 0
    users = []
    for user in userModel:
        name = user.firstname + ' ' + user.lastname
        for wallet in user.wallets:
            totAmt = totAmt + wallet.walletamt
            for utxn in wallet.txn:
                users.append({  "email": user.email, "name": name, "walletAmt": str(wallet.walletamt),
                                "txnDate": utxn.dated, "dailyAmt": str(utxn.txnamt),
                                "txnStatus":STATUS_CODE[str(utxn.status)].upper() })
            
    return { "admin":{ "totUsers": len(userModel), "totAmt": totAmt,
             "dailyUsers": 0, "dailyAmt": dailyAmt }, "usrDetails": users }