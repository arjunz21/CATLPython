import random
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from itsdangerous import URLSafeSerializer as Serializer

# import models
from models.fastModels import TokenData, User, UserInDB, UserWallet
from models.dbModels import UserModel
from components import walletapi
from sqlalchemy.orm import Session
from models import engine

# openssl rand -hex 32
SECRET_KEY = "72adde3fb62e9cb4bc456babc83fdfc5573219d841d9113bf8f9a0c5712b4b07"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db1 = Session(autocommit=False, autoflush=False, bind=engine)


def generateOTP():
    otpCode = random.randint(111111, 999999)
    return otpCode


def verifyOTP(otp, otpCode):
    if otp == otpCode:
        return True
    else:
        return False


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    userModel = db.query(UserModel).filter_by(email=email).first()
    if userModel is None:
        raise HTTPException(status_code=404, detail=f"User {email} does not exist")
    user = {"email": userModel.email, "firstname": userModel.firstname, "refcode": userModel.refcode,
            "lastname": userModel.lastname, "number": userModel.number, "invitecode": userModel.invitecode,
            "disabled": False, "imagefile": userModel.image_file, "admin": userModel.admin,
            "walletamt": str(userModel.wallets[0].walletamt)}
    return User(**user)


def authenticate_user(db: Session, email: str, password: str):
    userModel = db.query(UserModel).filter_by(email=email).first()
    if userModel is None:
        raise HTTPException(status_code=404, detail=f"User {email} does not exist")
    user = {"email": userModel.email, "firstname": userModel.firstname, "refcode": userModel.refcode,
            "lastname": userModel.lastname, "number": userModel.number, "invitecode": userModel.invitecode,
            "disabled": False, "imagefile": userModel.image_file}
    if not user:
        return False
    if not pwd_context.verify(password, userModel.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db1, email=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user.email


def create_user(db: Session, user: UserInDB):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        user = db.query(UserModel).filter_by(email=user.email).first()
        userwallet = UserWallet(walletamt="0", status="0", user_id=user.uid)
        walletapi.create_wallet(db, user.email, userwallet)
        return True
    except Exception as e:
        print("Error: ", e)
        return False


def delete_user(db: Session, email: str):
    userModel = db.query(UserModel).filter_by(email=email).first()
    if userModel is None:
        raise HTTPException(status_code=404, detail=f"User {email} does not exist")
    db.query(UserModel).filter_by(email=email).delete()
    db.commit()
    return {"status": "success"}
