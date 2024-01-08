#!/usr/bin/python
from hashlib import md5
from Crypto.Cipher import AES
from string import Template
from Crypto.Util.Padding import pad, unpad

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
#     data += chr(length) * length
#     return data


def encrypt(plainText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText.encode('utf-8'), AES.block_size)
    encDigest = md5()
    encDigest.update(workingKey.encode())
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
    encryptedText = enc_cipher.encrypt(plainText)
    return encryptedText


def decrypt(cipherText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = md5()
    decDigest.update(workingKey.encode())
    #encryptedText = cipherText.decode('hex')
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
    decryptedText = unpad(dec_cipher.decrypt(cipherText), AES.block_size)
    return decryptedText

e = encrypt("hello", "hi")
print(e)
print(decrypt(e, "hi"))