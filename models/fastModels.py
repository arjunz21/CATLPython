from pydantic import BaseModel


class FinPlan(BaseModel):
    planname: str | None = None
    status: int | None = 1
    price: int | None = None
    dailyincome: int | None = None
    days: int | None = None
    totalincome: int | None = None

    class Config:
        orm_mode: True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class User(BaseModel):
    number: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    invitecode: str | None = None
    refcode: str | None = None
    imagefile: str | None = "default.jpg"
    status: int | None = 1
    admin: bool | None = False
    disabled: bool | None = False

    class Config:
        orm_mode: True


class UserInDB(User):
    hashed_password: str


class UserBank(BaseModel):
    bankname: str | None = None
    bankaccnum: str | None = None
    bankifsccode: str | None = None
    user_id: int | None = None

    class Config:
        orm_mode: True


class UserWallet(BaseModel):
    wid: int | None = None
    walletamt: int | None = None
    status: int | None = 0
    user_id: int | None = None

    class Config:
        orm_mode: True

class SessionData(BaseModel):
    sessionid: str | None = None
    logintime: str | None = None
    logouttime: str | None = None
    ipaddr: str | None = None
    useragent: str | None = None
    user_id: int | None = None

    class Config:
        orm_mode: True


class UserFinTeamModel(BaseModel):
    dated: str | None = None
    plan: str | None = None
    number: str | None = None
    name: str | None = None
    email: str | None = None
    level: str | None = None

    class Config:
        orm_mode: True
