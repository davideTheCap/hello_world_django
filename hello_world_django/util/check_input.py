# from telethon import events, sync
from util.constants import *
# from bot.constants import *
from util.util import *
from util.constants import CheckConstant
from exceptions.custom_exceptions import *

import re
import datetime



def check_input_factory(type: str, **params):
    if type == CheckTravelRequestFields.TYPE:
        return CheckTravelRequestFields(**params)
    
    elif type == CheckEmail.TYPE:
        return CheckEmail(**params)  
    
    elif type == CheckCity.TYPE:
        return CheckCity(**params)

    elif type == CheckCountry.TYPE:
        return CheckCountry(**params)
    
    elif type == CheckActiveDiscount.TYPE:
        return CheckActiveDiscount(**params)

    elif type == CheckVerificationLink.TYPE:
        return CheckVerificationLink(**params)  

    elif type == CheckPolicy.TYPE:
        return CheckPolicy(**params)  
    
    elif type == CheckMemorandumFields.TYPE:
        return CheckMemorandumFields(**params)
    
    elif type == CheckMemorandumConfirmation.TYPE:
        return CheckMemorandumConfirmation(**params)
    
    elif type == CheckBotOtp.TYPE:
        return CheckBotOtp(**params)
    
    elif type == CheckTelegramVerification.TYPE:
        return CheckTelegramVerification(**params)

    else:
        return CheckInput()


class CheckInput:
    def __init__(self, **params):
        pass

    async def check(event, message):
        if isinstance(event, sync.Conversation):
            event.send_message("Something went wrong!")
        elif isinstance(event, events.NewMessage):
            await event.respond("Something went wrong!")


class CheckToDb(CheckInput):

    def __init__(self, **params):
        if params.get("db") is None:
            raise Exception("db not found!")
        
        self.db = params.get("db")
        
    
class CheckTravelRequestFields(CheckToDb):
    TYPE = CheckConstant.TRAVEL_REQ_FIELDS.value

    def check(self, form_fields):
        try:
            log.info("Checking user name..")
            user_name = form_fields['user_name']
            log.info(f"User name: {user_name}")
        
            log.info("Checking user_email and uni_domains..")
            email = form_fields['user_email']
            uni_domains = form_fields['uni_domains']
            checker = check_input_factory(CheckEmail.TYPE, db=self.db)
            email = f"{email}@{uni_domains}"
            checker.check(email)

            checker = check_input_factory(CheckUniDomain.TYPE, db=self.db)
            checker.check(email)

            checker = check_input_factory(CheckActiveDiscount.TYPE, db=self.db)
            checker.check(email)

            log.info("Checking home institution..")
            home_institution = form_fields['home_institution']
            log.info(f"Home institution: {home_institution}")
        
            log.info(f"Checking countries..")
            departure_country = form_fields['departure_country']
            arrival_country = form_fields['arrival_country']
            checker = check_input_factory(CheckCountry.TYPE, db=self.db)
            checker.check(departure_country)
            checker.check(arrival_country)
            log.info(f"Departure country: {departure_country}; Arrival country: {arrival_country}")

            log.info(f"Checking policy check..")
            policy_check = form_fields['policy_check']
            checker = check_input_factory(CheckPolicy.TYPE)
            checker.check(policy_check)
            log.info(f"Policy checked.")

        except KeyError as e:
            raise FieldNotFoundException(f"Form does not contain {e}")
        except Exception as e:
            log.exception(e)
            raise Exception(e)

class CheckEmail(CheckInput):
    TYPE = CheckConstant.USER_EMAIL.value

    def check(self, email):
        
        if email is None:
            raise Exception("Email not found!")
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Use re.match() to check if the email matches the pattern
        if not re.match(pattern, email):
            raise Exception("Email not valid")


class CheckUniDomain(CheckToDb):
    TYPE = CheckConstant.UNI_DOMAIN.value

    def check(self, email):
        log.info(f"Checking uni domain..")      

        if email is None:
            raise Exception("Email not found!")
        
        email_domain = email.split('@')[1]
        
        check_flag = self.db.check_uni_domain(email_domain)
        if not check_flag:
            raise InvalidUniDomainException("Invalid uni domain.")

class CheckActiveDiscount(CheckToDb):
    TYPE = CheckConstant.ACTIVE_DISCOUNT.value

    def check(self, email):
        
        if email is None:
            raise Exception("Email not found!")

        flag_active_discounts = self.db.check_active_discounts(email)
        
        if not flag_active_discounts:
            raise Exception("Too many active discount currently")
             
        return True
        
class CheckCity(CheckToDb):
    TYPE = CheckConstant.CITY.value
    # question = "Inserisci il la data di partenza con questo formato dd-mm-yyyy"

    def check(self, city):
        check_flag = self.db.check_city(city)
        if not check_flag:
            raise Exception("City not valid")
        
        return True


class CheckCountry(CheckToDb):
    TYPE = CheckConstant.COUNTRY.value

    def check(self, country):
        check_flag = self.db.check_country(country)
        if not check_flag:
            raise InvalidCountryException("Invalid country")

        return True


class CheckPolicy(CheckInput):
    TYPE = CheckConstant.POLICY.value
    checked = 'on'

    def check(self, policy):
        if policy != self.checked:
            raise Exception("Policy and TOS not accepted.")
        
        return True

class CheckMemorandumFields(CheckToDb):
    TYPE = CheckConstant.MEMORANDUM_REQ_FIELDS.value

    def check(self, form_fields):
        try:
            log.info("Checking email..")
            check_input_factory(CheckEmail.TYPE).check(form_fields.get('email'))

            log.info("Checking new university domain..")
            if self.db.check_memorandum(form_fields.get('uni_domain')):
                raise UniDomainAlreadyExistsException()

            log.info("Checking policy..")
            check_input_factory(CheckPolicy.TYPE).check(form_fields.get('policy_check'))
        except KeyError as e:
            raise Exception(f"Form does not contain {e}")
        except Exception as e:
            raise e

class CheckVerificationLink(CheckToDb):
    import hashlib
    import time

    TYPE = CheckConstant.VERIFICATION_LINK.value

    def check(self, token: str):         
        user = self.db.get_user_by_otp_hash(compute_hash(token))

        if not user:
            raise InvalidVerificationLink("Invalid token")

        log.info("Checking policy..")
        if time.time() - user.otp_created > 600:
            raise ExpiredTokenException("Verification link has expired.")
        
class CheckMemorandumConfirmation(CheckToDb):
    TYPE = CheckConstant.MEMORANDUM_CONFIRMATION

    def check(self, memorandum_uuid: str):
        if len(memorandum_uuid) != 36:
            raise InvalidIdException("Invalid memorandum uuid.")
        
        memorandum = self.db.get_memorandum(memorandum_uuid)

        if memorandum is None:
            raise MemorandumUuidNotFoundException()
        elif memorandum.confirmed is not None:
            raise MemorandumAlreadyConfirmedException()
        

    
class CheckBotOtp(CheckToDb):
    
    TYPE = CheckConstant.BOT_OTP_VERIFICATION

    def check(self, otp: str, telegram_id: str):

        stored_otp_hash = self.db.get_valid_otp_by_telegram_id(telegram_id)
        otp_hash = hashlib.sha512(otp.encode()).hexdigest()
        
        if otp_hash != stored_otp_hash:
            raise OtpVerificationFailedException()
        
        return True
        
class CheckTelegramVerification(CheckToDb):

    TYPE = CheckConstant.TELEGRAM_ID_VERIFICATION

    def check(self, telegram_id: str):
        return self.db.is_verified_user_by_telegram_id(telegram_id)