#!/usr/bin/python
from fastapi import APIRouter, Request
from string import Template
from fastapi.responses import HTMLResponse
from components.ccavHandler import res, encrypt
from fastapi.templating import Jinja2Templates

ccav_router = APIRouter(
    prefix='/api/ccav',
    tags=['CCAV']
)

templates = Jinja2Templates(directory="templates")
accessCode = 'AVAN40KL46BB14NABB'
workingKey = '97DC997FD024D2081D32B75072CAB101'


@ccav_router.get('/', response_class=HTMLResponse)
async def webpay(request: Request):
    return templates.TemplateResponse("dataFrom.htm", {"request": request})


@ccav_router.post('/Response')
async def payResponse(request: Request):
    plainText = res(request.form().get('encResp'))
    print("res: ", plainText)
    return plainText


@ccav_router.post('/ReqestHandler', response_class=HTMLResponse)
async def payRequest(request: Request):
    req = await request.form()
    p_merchant_id = req.get('merchant_id')

    merchant_data = {
   "merchant_id":req.get('merchant_id'),
   "order_id":req.get('order_id'),
   "currency":req.get('currency'),
   "amount":req.get('amount'),
   "redirect_url":req.get('redirect_url'),
   "cancel_url":req.get('cancel_url'),
   "language":req.get('language'),
   "billing_name":req.get('billing_name'),
   "billing_address":req.get('billing_address'),
   "billing_city":req.get('billing_city'),
   "billing_state":req.get('billing_state'),
   "billing_zip":req.get('billing_zip'),
   "billing_country":req.get('billing_country'),
   "billing_tel":req.get('billing_tel'),
   "billing_email":req.get('billing_email'),
   "delivery_name":req.get('delivery_name'),
   "delivery_address":req.get('delivery_address'),
   "delivery_city":req.get('delivery_city'),
   "delivery_state":req.get('delivery_state'),
   "delivery_zip":req.get('delivery_zip'),
   "delivery_country":req.get('delivery_country'),
   "delivery_tel":req.get('delivery_tel'),
   "merchant_param1":req.get('merchant_param1'),
   "merchant_param2":req.get('merchant_param2'),
   "merchant_param3":req.get('merchant_param3'),
   "merchant_param4":req.get('merchant_param4'),
   "merchant_param5":req.get('merchant_param5'),
   "integration_type":req.get('integration_type'),
   "promo_code":req.get('promo_code'),
   "customer_identifier":req.get('customer_identifier') }
    
    encryption = encrypt(merchant_data, workingKey)
    print(merchant_data)

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
