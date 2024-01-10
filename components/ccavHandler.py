#!/usr/bin/python
#from hashlib import md5
from Crypto.Cipher import AES
from string import Template
#from Crypto.Util.Padding import pad, unpad
import hashlib
from binascii import hexlify, unhexlify
from pay_ccavenue import CCAvenue

ccavenue = CCAvenue("97DC997FD024D2081D32B75072CAB101", "AVAN40KL46BB14NABB", "3098153", "https://catl.onrender.com/api/ccav/ResponseHandler", "https://catl.onrender.com/api/ccav/ResponseHandler")

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

def encrypt(plainText, workingKey):
    return ccavenue.encrypt(plainText)

def decrypt(cipherText, workingKey):
    return ccavenue.decrypt(cipherText)

d = {   "merchant_id":"3098153",
        "order_id":"123456",
        "currency":"INR",
        "amount":"1.00",
        "redirect_url":"/ResponseHandler",
        "cancel_url":"/ResponseHandler",
        "language":"EN",
        "integration_type":"iframe_normal" }

e = encrypt(d, "hi")
print(e)
print(decrypt({"encResp":"d378150482578dff21c054426a1bf38b6ef4bf1e87dd2ef12cc6d2ee1b446db47b20e462179e6f5eba118f0b8f506293e12d40ee6406afc68d4b2000a60dc37791a18c07f59d6f7cd78d93455b5d83ffb748b3c2ca1d577c4410bc6696b5f1006bd0855bef7898f29dac3ecc4588a927457594ab247b0bc773e3a0bd842fb33a7a0cb1ed3e6593a265eca5c3280b8c726b531ef19239372688d4cb82a2c658377db010c398b7f507379b2e9f9a95d65eb7a0b66589027a45339f596ba20782c68fff5c9ad632d025c0317ad623a92078e5bdb8388a1366151f37ab6d2b4dec51fc5c4a6cf459d08e4c0bfe4637590b113613e9be52ff0262453f362506611a09a327cad07153efa96dd4e28087a9d67eeec720d99676385e4beea046360eb98a54623864fbff199d5ef42b82f033e77ffe68392d614d3ff07f953683d71bb04578f5cb5f672c396d8a0d49b319b78fece900d2ea8e36ba41cb6d25165f5a85592e7418d1b62939234a2f0e01a116789ecf4ae3f28be7553b282d4115387cceab14850fa6f1488b0b0d2e21cfc4760129829a50cc9840efa0d48f07c8969949dbe4185ce4ede27c84f9d7f20013698aab140e50106345b197de8c72b67970ef5bd0703af9ae4989ceb2e3184bb9a07e3a7b63564dac92f2474b7c105eccb04a930cd5effe41b339d790bf0b37063b08b49aca6f54177141a37bad177052bf1b11a809929216b64a085bab029fcbc84080"}, "hi"))
