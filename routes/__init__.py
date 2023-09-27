from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

import models
from components import authenticapi
from sqlalchemy.orm import Session

from models.dbModels import UserModel
from models.fastModels import Token, User, UserInDB, FinPlan, UserBank, UserWallet, UserFinTeamModel

ACCESS_TOKEN_EXPIRE_MINUTES = 30
models.Base.metadata.create_all(bind=models.engine)
