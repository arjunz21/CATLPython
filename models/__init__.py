#import psycopg2
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://uddvrzdwlzy9qmy:UWAkLaeASbyod4A2brzg@bjak0ygef1mx1rbc9yfm-mysql.services.clever-cloud.com:3306/bjak0ygef1mx1rbc9yfm'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/catl'
#PGPASSWORD=nwzSXdiu]]iuo][p['i[[;. kimlmp j'- ik,mbgn g3umHFPfcUWMXyZ1qiLRdTcmdI psql -h dpg-clta81da73kc73efr980-a.oregon-postgres.render.com -U catluser catldb
#SQLALCHEMY_DATABASE_URI = 'postgresql://catluser:nwzSXdg3umHFPfcUWMXyZ1qiLRdTcmdI@dpg-clta81da73kc73efr980-a.oregon-postgres.render.com:5432/catldb'
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(getdb)]

# import secrets
# secrets.token_hex(16)
# hashed_pwd = bcrypt.generate_password_hash('testing')
# bcrypt.generate_password_hash('testing').decode('utf-8')
# bcrypt.check_password_hash(hashed_pwd, 'testing')
# from main import app, db
# from main.models import Usermodel, Walletmodel, Financeplanmodel, Userbankmodel
# db.create_all()
# usr_1 = Usermodel(username='john.doe', password='pwd', number='0123456789', firstname='John', lastname='Doe', email='john.doe@a.com', invitecode='code123')
# fin_1 = Financeplanmodel(planname='NORMAL', price=17800, dailyincome=533, totalincome=150, days=300, user_id=usr1.uid)
# wallet_1 = Walletmodel(walletamt='0', status='created',user_id=usr1.uid)
# bank_1 = Userbankmodel(bankname='SBI', bankaccnum='sbi123abc456', bankifsccode='SBI123', user_id=usr1.uid)
# db.session.add(user_1)
# db.session.commit()
# db.session.rollback()
# Usermodel.query.all()
# Usermodel.query.filter_by(username='john.doe').first()
# Usermodel.query.get(1)
