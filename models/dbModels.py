from sqlalchemy import Table, Column, Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from datetime import datetime
from models import Base


userteam_table = Table('userteam', Base.metadata,
    Column('user_id', ForeignKey('user.uid')),
    Column('fin_id', ForeignKey('financeplan.fid')),
    Column('dated', DateTime, nullable=False, default=datetime.utcnow),
    Column('status', Integer, default=1)
)


# models for database
class Financeplanmodel(Base):
    __tablename__ = "financeplan"
    fid = Column(Integer, primary_key=True)
    dated = Column(DateTime, nullable=False, default=datetime.utcnow)
    planname = Column(String(30), unique=True, nullable=False)
    status = Column(Integer, default=1)
    price = Column(Integer, nullable=False)
    dailyincome = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    members = relationship('UserModel',
                            secondary=userteam_table,
                            back_populates='finplans')
    
    def __repr__(self):
        return f"Plan('{self.planname}', '{self.members}')"


class UserModel(Base):
    __tablename__ = "user"
    uid = Column(Integer, primary_key=True, index=True)
    dated = Column(DateTime, nullable=False, default=datetime.utcnow)
    password = Column(String(60), nullable=False)
    number = Column(String(10), unique=True, nullable=False)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    invitecode = Column(String(10), nullable=True)
    refcode = Column(String(10), nullable=False)
    image_file = Column(String(20), default='default.jpg')
    admin = Column(Boolean, nullable=False, default=False)
    status = Column(Integer, default=1)
    banks = relationship('Userbankmodel', back_populates='user')
    wallets = relationship('Walletmodel', back_populates='user')
    sessions = relationship('Sessiondatamodel', back_populates='user')
    finplans = relationship('Financeplanmodel',
                            secondary=userteam_table,
                            back_populates='members')
    
    def __repr__(self):
        return f"User('{self.email}', '{self.invitecode}', '{self.refcode}')"


class Userbankmodel(Base):
    __tablename__ = "userbank"
    bid = Column(Integer, primary_key=True)
    dated = Column(DateTime, nullable=False, default=datetime.utcnow)
    bankname = Column(String(30), nullable=False)
    bankaccnum = Column(String(30), unique=True, nullable=False)
    bankifsccode = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey('user.uid'), nullable=False)
    user = relationship('UserModel', back_populates='banks')

    def __repr__(self):
        return f"Bank('{self.bankname}', '{self.bankifsccode}', '{self.bankaccnum}')"


class Walletmodel(Base):
    __tablename__ = "wallet"
    wid = Column(Integer, primary_key=True)
    dated = Column(DateTime, nullable=False, default=datetime.utcnow)
    walletamt = Column(Integer, nullable=False, default=0)
    status = Column(Integer, default=4)
    user_id = Column(Integer, ForeignKey('user.uid'), nullable=False)
    user = relationship('UserModel', back_populates='wallets')
    txn = relationship('Txnmodel', back_populates='wallets')

    def __repr__(self):
        return f"Wallet('{self.user_id}', '{self.walletamt}', '{self.status}')"


class Txnmodel(Base):
    __tablename__ = "transaction"
    txnid = Column(Integer, primary_key=True)
    dated = Column(DateTime, nullable=False, default=datetime.utcnow)
    txnamt = Column(Integer, nullable=False, default=0)
    txntype = Column(String(3), nullable=False)
    summary = Column(String(60), nullable=True)
    rcptno = Column(String(30), unique=True, nullable=False) 
    number = Column(String(10), nullable=False)
    status = Column(Integer, default=4)
    wallet_id = Column(Integer, ForeignKey('wallet.wid'), nullable=False)
    wallets = relationship('Walletmodel', back_populates='txn')

    def __repr__(self):
        return f"Txn('{self.wallet_id}', '{self.txnamt}', '{self.status}')"


class Sessiondatamodel(Base):
    __tablename__ = "sessiondata"
    sessionid = Column(Integer, primary_key=True)
    logintime = Column(DateTime, nullable=False, default=datetime.utcnow)
    logouttime = Column(DateTime, nullable=True)
    ipaddr = Column(String(20), nullable=False)
    useragent = Column(String(60), nullable=False)
    user_id = Column(Integer, ForeignKey('user.uid'), nullable=False)
    user = relationship('UserModel', back_populates='sessions')
