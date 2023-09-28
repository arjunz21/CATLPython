import os
import ssl
import random
import imghdr
import smtplib
from itsdangerous import URLSafeSerializer
from twilio.rest import Client
from email.message import EmailMessage

# Thanks! If there's an account associated with this email, we'll send the password reset instructions immediately.


STATUS_CODE = {
    "0": "success", "1": "active", "2": "suspend", "3": "inactive",
    "4": "creating", "5": "cancelled", "6": "failed",
    "7": "pending", "8": "refunded", "9": "abandoned"
}

STATUS_COLOR = {
    "0": "success", "1": "primary", "2": "secondary", "3": "dark",
    "4": "info", "5": "danger", "6": "danger",
    "7": "warning", "8": "secondary", "9": "danger"
}


class Config:
    ACCSID = 'AC98ed2d67c489696cdc3365232fa90bba'
    AUTHTOKEN = 'c5a51d7efb48938dca5229a46870ca86'
    VERIFY_SID = "VAe0b2044421ec253a5d6f2de99bc36a6f"
    VERIFIED_NUMBER = "+918861582104"
    EMAIL_ADDRESS = 'arjun.gadvi@gmail.com'
    EMAIL_PASSWORD = 'samqsqzjbhhzescl'
    # ACCSID = os.getenv('ACCSID')
    # AUTHTOKEN = os.getenv('AUTHTOKEN')
    # VERIFY_SID = os.getenv('VERIFY_SID')
    # VERIFIED_NUMBER = os.getenv('VERIFIED_NUMBER')
    # EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    # EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    FROM_EMAIL = 'catl@noreply.com'


class SafeURL:
    auth_s = URLSafeSerializer("secret key", "auth")
    token = auth_s.dumps({"id": 5, "name": "itsdangerous"})

    # print(token)
    # eyJpZCI6NSwibmFtZSI6Iml0c2Rhbmdlcm91cyJ9.6YP6T0BaO67XP--9UzTrmurXSmg

    data = auth_s.loads(token)
    # print(data["name"]) # itsdangerous


class SendMail:

    def sendEmail(self, toEmail, subject, body, file=None, link=None):
        msg = EmailMessage()
        msg['From'] = Config.FROM_EMAIL
        msg['To'] = toEmail
        msg['Subject'] = subject
        msg.set_content(body)
        context = ssl.create_default_context()

        if file:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        if link:
            msg.add_alternative(f"<a href='{link}' />", subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
            smtp.sendmail(Config.EMAIL_ADDRESS, toEmail, msg.as_string())


class OTPGenerate:

    def __init__(self) -> None:
        self.client = Client(Config.ACCSID, Config.AUTHTOKEN)
        # self.accsid = Config.accsid
        # self.auth_token = Config.authtoken
        # self.client=Client(self.accsid, self.auth_token)

    def sendOTP(self):
        # self.n = random.randint(1111,9999)
        # self.client.messages.create(to=[""], from_="", body=self.n)
        verification = self.client.verify.v2.services(self.verify_sid).verifications.create(to=self.verified_number,
                                                                                            channel="sms")
        print(verification.status)

# sendmail = SendMail()
# sendmail.sendEmail('arjun.gadvi@gmail.com', 'Grab the Offer', 'Offer Time is very limited')
# otp = OTPGenerate()
# otp.sendOTP()
# Set environment variables for your credentials
# Read more at http://twil.io/secure
# otp_code = input("Please enter the OTP:")
# verification_check = client.verify.v2.services(verify_sid) \
#   .verification_checks \
#   .create(to=verified_number, code=otp_code)
# print(verification_check.status)
