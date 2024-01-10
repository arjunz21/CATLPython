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
from routes.ccavMain import ccav_router
from components.commonutils import SendMail
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from fastapi.templating import Jinja2Templates
from fastapi import Request
from string import Template
from fastapi.responses import HTMLResponse
from components.ccavHandler import res, encrypt

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
app.include_router(ccav_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

from routes import Annotated, Depends, Session, status, timedelta, HTTPException
from routes import Token, User, UserModel, UserInDB, models, authenticapi
from routes import OAuth2PasswordRequestForm, ACCESS_TOKEN_EXPIRE_MINUTES


@app.get("/app", response_class=RedirectResponse)
async def mainapp():
    return "/static/index.html"


# UserModel Start
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
    sendmail.sendEmail(email, 'Welcome to CATL Group - OTP Confirmation', subject)
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


@app.get('/', response_class=HTMLResponse)
async def webpay(request: Request):
    return templates.TemplateResponse("dataFrom.htm", {"request": request})


@app.post('/Response')
async def payResponse(request: Request):
    plainText = res(request.form().get('encResp'))
    print("res: ", plainText)
    return plainText


@app.post('/ReqestHandler', response_class=HTMLResponse)
async def payRequest(request: Request):
    req = await request.form()
    p_merchant_id = req.get('merchant_id')
    p_order_id = req.get('order_id')
    p_currency = req.get('currency')
    p_amount = req.get('amount')
    p_redirect_url = req.get('redirect_url')
    p_cancel_url = req.get('cancel_url')
    p_language = req.get('language')
    p_billing_name = req.get('billing_name')
    p_billing_address = req.get('billing_address')
    p_billing_city = req.get('billing_city')
    p_billing_state = req.get('billing_state')
    p_billing_zip = req.get('billing_zip')
    p_billing_country = req.get('billing_country')
    p_billing_tel = req.get('billing_tel')
    p_billing_email = req.get('billing_email')
    p_delivery_name = req.get('delivery_name')
    p_delivery_address = req.get('delivery_address')
    p_delivery_city = req.get('delivery_city')
    p_delivery_state = req.get('delivery_state')
    p_delivery_zip = req.get('delivery_zip')
    p_delivery_country = req.get('delivery_country')
    p_delivery_tel = req.get('delivery_tel')
    p_merchant_param1 = req.get('merchant_param1')
    p_merchant_param2 = req.get('merchant_param2')
    p_merchant_param3 = req.get('merchant_param3')
    p_merchant_param4 = req.get('merchant_param4')
    p_merchant_param5 = req.get('merchant_param5')
    p_integration_type = req.get('integration_type')
    p_promo_code = req.get('promo_code')
    p_customer_identifier = req.get('customer_identifier')

    merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&' + 'language=' + p_language + '&' + 'billing_name=' + p_billing_name + '&' + 'billing_address=' + p_billing_address + '&' + 'billing_city=' + p_billing_city + '&' + 'billing_state=' + p_billing_state + '&' + 'billing_zip=' + p_billing_zip + '&' + 'billing_country=' + p_billing_country + '&' + 'billing_tel=' + p_billing_tel + '&' + 'billing_email=' + p_billing_email + '&' + 'delivery_name=' + p_delivery_name + '&' + 'delivery_address=' + p_delivery_address + '&' + 'delivery_city=' + p_delivery_city + '&' + 'delivery_state=' + p_delivery_state + '&' + 'delivery_zip=' + p_delivery_zip + '&' + 'delivery_country=' + p_delivery_country + '&' + 'delivery_tel=' + p_delivery_tel + '&' + 'merchant_param1=' + p_merchant_param1 + '&' + 'merchant_param2=' + p_merchant_param2 + '&' + 'merchant_param3=' + p_merchant_param3 + '&' + 'merchant_param4=' + p_merchant_param4 + '&' + 'merchant_param5=' + p_merchant_param5 + '&' + 'integration_type=' + p_integration_type + '&' + 'promo_code=' + p_promo_code + '&' + 'customer_identifier=' + p_customer_identifier + '&'
    # print("mer:", merchant_data)
    encryption = encrypt(merchant_data, workingKey)

    html = '''\
        <html>
        <head>
            <title>Sub-merchant checkout page</title>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        </head>
        <body>
            <center>
            <!-- width required mininmum 482px -->
                <iframe  width="482" height="500" scrolling="No" frameborder="0"  id="paymentFrame" src="https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction&merchant_id=$mid&encRequest=$encReq&access_code=$xscode">
                </iframe>
            </center>
            
            <script type="text/javascript">
                $(document).ready(function(){
                    $('iframe#paymentFrame').load(function() {
                        window.addEventListener('message', function(e) {
                            $("#paymentFrame").css("height",e.data['newHeight']+'px'); 	 
                        }, false);
                    }); 
                });
            </script>
        </body>
        </html>
        '''
    fin = Template(html).safe_substitute(mid=p_merchant_id,encReq=encryption,xscode=accessCode)
    return fin
    # return templates.TemplateResponse('merPage.htm', {"request":req, "mid":p_merchant_id,"encReq":merchant_data, "xscode":accessCode})
