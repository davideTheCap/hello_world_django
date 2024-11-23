import os
from enum import Enum

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

GO2RAIL_PHONE_NUM = os.getenv("GO2RAIL_PHONE_NUM")
GO2RAIL_EMAIL = os.getenv("GO2RAIL_EMAIL")

VERIFICATION_LINK_PATH = os.getenv("VERIFICATION_LINK_PATH")
# GMAIL_CREDENTIALS_PATH = os.getenv(GMAIL_CREDENTIALS_PATH)

class CheckConstant(Enum):
    TRAVEL_NAME = "travel_name"
    TRAVEL_DEPARTURE_DATE = "travel_departure_date"
    TRAVEL_DEPARTURE_CITY = "travel_departure_city"
    TRAVEL_ARRIVAL_CITY = "travel_arrival_city"
    USER_EMAIL = "email"
    UNI_DOMAIN = 'uni_domain'
    ACTIVE_DISCOUNT = 'active_discount'
    CITY = "city"
    COUNTRY = "country"
    POLICY = "policy"
    TRAVEL_REQ_FIELDS = "travel_request_fields"
    MEMORANDUM_REQ_FIELDS = "memorandum_req_fields"
    TRAVEL_REQUEST_VERIFICATION = 'travel_request_verification'
    VERIFIED_EMAIL = 'verified_email'
    VERIFICATION_LINK = 'verification_link'
    MEMORANDUM_CONFIRMATION = "memorandum_confirmation"

    BOT_OTP_VERIFICATION = "otp_verification" 
    TELEGRAM_ID_VERIFICATION = 'telegram_id_verification'


class EmailTemplateManagerConstant(Enum):
    TRAVEL_REQUEST_VERIFICATION = "verification_email"
    MEMORANDUM_REQ = "memorandum_request"
    MEMORANDUM_CONFIRMATION = "memorandum_confirmation"
    BOT_OTP_GENERATION = "otp_generation"
    BOT_OTP_VERIFICATION = "otp_verification"

