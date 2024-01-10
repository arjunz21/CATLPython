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
        "order_id":req.get('order_id'),
        "amount":req.get('amount'),
        "customer_identifier":req.get('customer_identifier'),
        "billing_name":req.get('billing_name'),
        "billing_email":req.get('billing_email'),
        "currency":'INR',
        "language":'EN',
        "integration_type":'iframe_normal'
    }
    encryption = encrypt(merchant_data, workingKey)

    html = '''\
        <html>
        <head>
            <title>Payment Page</title>
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
