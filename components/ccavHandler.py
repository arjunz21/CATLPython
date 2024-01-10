#!/usr/bin/python
#from hashlib import md5
from Crypto.Cipher import AES
from string import Template
#from Crypto.Util.Padding import pad, unpad
import hashlib
from binascii import hexlify, unhexlify
from pay_ccavenue import CCAvenue

def res(encResp):
    '''Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.'''
    workingKey = '97DC997FD024D2081D32B75072CAB101'
    decResp = decrypt(encResp, workingKey)
    data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'
    data = data + decResp.replace('=', '</td><td>')
    data = data.replace('&', '</td></tr><tr><td>')
    data = data + '</td></tr></table>'

    html = '''<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
			<title>Response Handler</title>
		</head>
		<body>
			<center>
				<font size="4" color="blue"><b>Response Page</b></font>
				<br>
				$response
			</center>
			<br>
		</body>
	</html>'''

    fin = Template(html).safe_substitute(response=data)
    return fin


# def pad(data):
#     length = 16 - (len(data) % 16)
#     data += chr(length)*length
#     return data

# def unpad(data):
#     return data[0:-ord(data[-1])] 

# def encrypt(plainText, workingKey):
#     iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'.encode("utf-8")
#     plainText = pad(plainText)
#     bytearrayWorkingKey = bytearray()
#     bytearrayWorkingKey.extend(map(ord, workingKey))
#     enc_cipher = AES.new(hashlib.md5(bytearrayWorkingKey).digest(), AES.MODE_CBC, iv)
#     return hexlify(enc_cipher.encrypt(plainText.encode("utf-8"))).decode('utf-8')

# def decrypt(cipherText, workingKey):
#     iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'.encode("utf-8")
#     encryptedText = unhexlify(cipherText)
#     bytearrayWorkingKey = bytearray()
#     bytearrayWorkingKey.extend(map(ord, workingKey))
#     decCipher = AES.new(hashlib.md5(bytearrayWorkingKey).digest(), AES.MODE_CBC, iv)
#     return unpad(decCipher.decrypt(encryptedText).decode('utf-8'))

ccavenue = CCAvenue("97DC997FD024D2081D32B75072CAB101", "AVAN40KL46BB14NABB", "3098154", "https://catl.onrender.com/api/ccav/ResponseHandler", "https://catl.onrender.com/api/ccav/ResponseHandler")

def encrypt(plainText, workingKey):
    return ccavenue.encrypt(plainText)

def decrypt(cipherText, workingKey):
    return ccavenue.decrypt(cipherText)

d = {
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

e = encrypt(d, "hi")
print(e)
print(decrypt({"encResp":"d378150482578dff21c054426a1bf38b61c7411456c40ac9532f843dbbf3413121340fcbf17d238d2fbc572ae6e21eb57e39197da01e161abeaf98e2dd350fd3451856e1cda8fe85d724297a2cbb4180a18f7af0d9dc665c94ad0552389964f28e7647c0b69f2373ba68d7f9ff6ec14ee2b4447f7221ee23eb89951221154d16251e33ce4058f63f147bc0c8533b17c4d4254087a2f5dca10305e3e3f17ef04a36a87314e3bc500c4b963a2ba8f385cb8773f55e9798eaf50a2702accdc619d3ad555b6010508d657c25a52385e74af53283b3ee26beb1f83a5e5610e4a512e6dc414f396734cd5eb779ecf8ac4a0f93ebabe3f5f23b28fbf5a02f8763ce7750fe0abcd75cbb3f9f293f8f958ea09892fe66bc471c49fd8019ee34c73bb8cf5e5e811373f00cbcdf0d786f68ba6c68ad887931b34e1ef8343db48baa5c99068d7889021cd69d1f113e1c4e261e6a426969ec80071105645ebcbdcf517d6eef0a459c204c78f4829d1c011658f6251b7eb68bee4b37043bf3520583f54507c9e69590f44a06b1aa90632cb00d2e967fa54770761a0e6dbd8b9e1838cbf648d6fb49945cee48566f5a32a1fbe0cca74408234779dcf9e5f3037ab97f6d5009a3bf8fe50c78bb7da4a07752c567bb8a161d89f054f5dbe4d90d121e2e5a67282a27440e06e3d42b32fa7c6e209014b92d52f4175845c9cb7081e2b44d74c9487afde9c81e409308bde90ace5087bc5ff2b39642b6515c58f57c2d787fcba21078e346b96ca7e80958981a46ecea1328ad0a80e7fe8b05248014ed4d20c6c556afb2633d1210493a757b8d72e24e9ca8abd5c85a6f4e1c66408210ecfcdb4f7562785f0765273ecb0723776857093b16e6a21cd446ea9103f300e73e95b2af6ddefccc137a6f708f25b346ad81449699f7a4762084fc4a539baa84bb425c30df55dd42c608916dcb572c4120a276978004188de03d38bd00350efa34910b79c1234af0e67ee9470a50d97e8a63f6bbb8ecd831b599bf939fb1c977cc17ce0b5115361e087225ec66d478bd12de7798b58b5c54f8b8a49d368464bc15cea573dde130a85ae56ff9b7f66b6a51c86b17b8793c0a07bc26fc1efa80d825298879024a05"}, "hi"))
