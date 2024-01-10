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

    #merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&' + 'language=' + p_language + '&' + 'billing_name=' + p_billing_name + '&' + 'billing_address=' + p_billing_address + '&' + 'billing_city=' + p_billing_city + '&' + 'billing_state=' + p_billing_state + '&' + 'billing_zip=' + p_billing_zip + '&' + 'billing_country=' + p_billing_country + '&' + 'billing_tel=' + p_billing_tel + '&' + 'billing_email=' + p_billing_email + '&' + 'delivery_name=' + p_delivery_name + '&' + 'delivery_address=' + p_delivery_address + '&' + 'delivery_city=' + p_delivery_city + '&' + 'delivery_state=' + p_delivery_state + '&' + 'delivery_zip=' + p_delivery_zip + '&' + 'delivery_country=' + p_delivery_country + '&' + 'delivery_tel=' + p_delivery_tel + '&' + 'merchant_param1=' + p_merchant_param1 + '&' + 'merchant_param2=' + p_merchant_param2 + '&' + 'merchant_param3=' + p_merchant_param3 + '&' + 'merchant_param4=' + p_merchant_param4 + '&' + 'merchant_param5=' + p_merchant_param5 + '&' + 'integration_type=' + p_integration_type + '&' + 'promo_code=' + p_promo_code + '&' + 'customer_identifier=' + p_customer_identifier + '&'
    merchant_data = {
   "merchant_id":"3098154",
   "order_id":"123456",
   "currency":"INR",
   "amount":"1.00",
   "redirect_url":"https://catl.onrender.com/api/ccav/ResponseHandler",
   "cancel_url":"https://catl.onrender.com/api/ccav/ResponseHandler",
   "language":"EN",
   "billing_name":"Peter",
   "billing_address":"Santacruz",
   "billing_city":"Mumbai",
   "billing_state":"MH",
   "billing_zip":"400054",
   "billing_country":"India",
   "billing_tel":"0229874789",
   "billing_email":"testing@domain.com",
   "delivery_name":"Sam",
   "delivery_address":"Vile Parle",
   "delivery_city":"Mumbai",
   "delivery_state":"Maharashtra",
   "delivery_zip":"400038",
   "delivery_country":"India",
   "delivery_tel":"0221234321",
   "merchant_param1":"additional Info.",
   "merchant_param2":"additional Info.",
   "merchant_param3":"additional Info.",
   "merchant_param4":"additional Info.",
   "merchant_param5":"additional Info.",
   "integration_type":"iframe_normal",
   "promo_code":"",
   "customer_identifier":""
}
    # print("mer:", merchant_data)
    encryption = encrypt(merchant_data, workingKey)
    print(req)

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
