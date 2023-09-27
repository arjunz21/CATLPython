from routes import Annotated, Depends, Session, status, timedelta, HTTPException
from routes import Token, User, UserModel, UserInDB, models, authenticapi
from routes import OAuth2PasswordRequestForm, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter


auth_router = APIRouter(
    prefix='/api/auth',
    tags=['Authentication']
)


# UserModel start
@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(models.getdb)):
    user = authenticapi.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Username or Password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = authenticapi.create_access_token(data={"sub": user["username"]},
                                                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=access_token, token_type="Bearer")


@auth_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(authenticapi.get_current_active_user)):
    return current_user


@auth_router.put("/users/register/", response_model=User)
async def create_user(user: UserInDB, db: Session = Depends(models.getdb)):
    userToDB = UserModel(username=user.username, password=authenticapi.get_password_hash(user.hashed_password),
                         number=user.number, firstname=user.firstname, lastname=user.lastname, email=user.email,
                         invitecode=user.invitecode, image_file=user.imagefile)
    authenticapi.create_user(db, userToDB)
    return userToDB


@auth_router.delete("/user/")
def delete_user(username: str, db: Session = Depends(models.getdb),
                current_user: User = Depends(authenticapi.get_current_active_user)):
    return authenticapi.delete_user(db, username)

# UserModel end