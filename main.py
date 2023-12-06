# import uvicorn
import random
from os import getenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
#from starlette.middleware import Middleware
#from starlette.middleware.cors import CORSMiddleware

from models import Base, engine
from routes.bank_routes import bank_router
from routes.finplan_routes import finplan_router
from routes.wallet_routes import wallet_router
from routes.userfinteam_routes import userfinteam_router
from routes.admidashroutes import admindash_router
from components.commonutils import SendMail
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

otpCode = 0
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://0.0.0.0', 'http://0.0.0.0:8000',
                   'http://fedora', 'http://fedora:8000',
                   'https://catlweb.onrender.com', 'https://catlweb.onrender.com:443',
                   'http://objective-violet-87944.pktriot.net:22010', ],
    allow_credentials=True, allow_methods=['*'], allow_headers=['*']
)

app.include_router(bank_router)
app.include_router(finplan_router)
app.include_router(wallet_router)
app.include_router(userfinteam_router)
app.include_router(admindash_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

from routes import Annotated, Depends, Session, status, timedelta, HTTPException
from routes import Token, User, UserModel, UserInDB, models, authenticapi
from routes import OAuth2PasswordRequestForm, ACCESS_TOKEN_EXPIRE_MINUTES


@app.get("/", response_class=RedirectResponse)
async def mainapp():
    return "/static/index.html"


# UserModel start
@app.post("/api/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(models.getdb)):
    user = authenticapi.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Username or Password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = authenticapi.create_access_token(data={"sub": user["email"]},
                                                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/api/users/me/", tags=["Authentication"])
async def read_users_me(current_user: str = Depends(authenticapi.get_current_active_user)):
    return current_user


@app.get("/api/users/me/info", tags=["Authentication"])
async def read_user(db: Session = Depends(models.getdb),
                    current_user: str = Depends(authenticapi.get_current_active_user)):
    return authenticapi.get_user(db, current_user)


@app.get("/api/users/generateotp", tags=["Authentication"])
async def generate_otp(email):
    otpCode = authenticapi.generateOTP()
    subject = f""""
    Hi,
    
    Welcome to CATL!

    Enter the OTP Code - OTP {otpCode}

    Have questions on using CATL application? Send us email at support@catl.com.

    Cheers!
    The CATL Team
    """
    sendmail = SendMail()
    sendmail.sendEmail(email,
                       'Welcome to CATL Group - OTP Confirmation',
                       subject)
    return {"email": email, "code": otpCode}


@app.put("/api/users/register/", response_model=User, tags=["Authentication"])
async def create_user(user: UserInDB, db: Session = Depends(models.getdb)):
    userToDB = UserModel(email=user.email, password=authenticapi.get_password_hash(user.hashed_password),
                         number=user.number, firstname=user.firstname, lastname=user.lastname,
                         invitecode=user.invitecode.upper(), image_file=user.imagefile,
                         refcode="INV"+str(random.randint(111111, 999999)), admin=user.admin, status=user.status)
    authenticapi.create_user(db, userToDB)
    subject = f""""
    Greetings {user.firstname} {user.lastname},
    
    Welcome to CATL!
    
    To activate your CATL Account, please verify your email address.
    Your account will not be created until your email address is confirmed.

    Have questions on using CATL application? Send us email at support@catl.com.

    Cheers!
    The CATL Team
    """
    sendmail = SendMail()
    sendmail.sendEmail(user.email,
                    'Welcome to CATL Group',
                    subject)
    return user


@app.delete("/api/user/", tags=["Authentication"])
def delete_user(username: str, db: Session = Depends(models.getdb),
                current_user: str = Depends(authenticapi.get_current_active_user)):
    return authenticapi.delete_user(db, username)


@app.post("/api/users/session/", tags=["Authentication"])
async def read_users_me(current_user: str = Depends(authenticapi.get_current_active_user)):
    return current_user


@app.patch("/api/users/resetpassword/", tags=["Authentication"])
async def read_users_me(current_user: str = Depends(authenticapi.get_current_active_user)):
    return current_user

# UserModel end


# if __name__ == '__main__':
#     uvicorn.run("main:app",
#                 port=443, host='fedora', reload = True, reload_dirs = ["html_files"],
#                 ssl_keyfile="/workshop/react/InvestApp/investreact/ssl/catlkey.pem",
#                 ssl_certfile="/workshop/react/InvestApp/investreact/ssl/catlcert.pem")

# if __name__ == '__main__':
#     port = int(getenv("PORT", 8000))
#     uvicorn.run("main:app",port=port, host='0.0.0.0', reload = True, reload_dirs = ["html_files"])
