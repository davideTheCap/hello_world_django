import logging
import hashlib
import requests

from exceptions.custom_exceptions import OtpVerificationFailedException

format = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(lineno)d] [%(levelname)-5.5s]  %(message)s"
)
log = logging.getLogger()

# fileHandler = logging.FileHandler(f"/log/bot2rail.log")
# fileHandler.setFormatter(format)
# log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(format)
log.addHandler(consoleHandler)


import re


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


import random


def generate_otp():
    import pyotp
    
    otp = pyotp.TOTP('base32secret3232').now()
    return otp

def verify_otp(otp: str, stored_otp_hash: str):

    

    otp_hash = hashlib.sha512(otp.encode()).hexdigest()
    
    if otp_hash != stored_otp_hash:
        raise OtpVerificationFailedException()
    
    return True


def compute_hash(otp: str):
    sha256_hash = hashlib.sha512()
    sha256_hash.update(otp.encode('utf-8'))
    return sha256_hash.hexdigest()


async def ask_question(conv, message):
    await conv.send_message(message)
    travel_plan_event = await conv.get_response()
    return travel_plan_event.message


url = "https://hook.eu1.make.com/8x9eqhilpwqdd5kudvqfh2ovqthaeadj" # os.environ['SEND_EMAIL_WEBHOOK']


def send_email(from_email, to_email, subject, content, attachment_path=None):
    try:
        data = {
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "content": content
        }

        attachment = {'attachment': open(attachment_path, 'rb')} if attachment_path else None
        response = requests.post(url, json=data, files=attachment, timeout=5)

        return response.status_code == 200
    except Exception as e:
        raise e



