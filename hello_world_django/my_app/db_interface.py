from peewee import *
from datetime import datetime

from my_app.models import *
from util.util import log
from uuid import uuid4
from exceptions.custom_exceptions import ExpiredOtpException


class DbInterface:
    def __init__(
        self, hostname: str, db_name: str, user: str, password: str, port: int
    ) -> None:
        self.hostname = hostname
        self.db_name = db_name
        self.db_user = user
        self.db_password = password
        self.port = port

    def process_request(self, request):
        self.db.connect()

    def process_response(self, request, response):
        if not self.db.is_closed():
            self.db.close()
        return response


class MySqlInterface(DbInterface):
    
    def __init__(self, db_name: str, user: str, password: str, hostname: str = "localhost", port: int = 3306) -> None:
        self.__check_construction_values(hostname, db_name, user, password, port)
        super().__init__(
            hostname=hostname, db_name=db_name, user=user, password=password, port=port
        )

        print("Connecting to the database..")
        self.db = MySQLDatabase(
            self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.hostname,
            port=self.port,
        ) 

    def __init__(self) -> None:
        self.db = model_database    


    def __check_construction_values(self, hostname: str, db_name: str, user: str, password: str, port: int):
        if not port or int(port) < 0:
            log.info(f"Port number {port}. Replaced with default value.")
            port = 3306

    def get_user_by_id(self, uuid: str) -> Users:
        return Users.get_by_id(uuid)

    def get_user_by_email(self, email: str) -> Users:
        return Users.get_or_none(Users.email == email)

    def get_user_by_telegram_id(self, telegram_id: str) -> Users:
        return Users.get_or_none(Users.telegram_user_id == telegram_id)

    def get_user_by_email_telegram_id(self, email, telegram_id: str) -> Users:
        return Users.get_or_none(
            Users.email == email & Users.telegram_user_id == telegram_id
        )

    def get_all_users(self) -> Users:
        return Users.select()

    def edit_user_by_id(self) -> Users:
        return Users.replace()

    def delete_user_by_id(self, uuid: str) -> None:
        Users.delete_by_id(uuid)

    def get_otp_by_user(self, uuid: str):
        return self.get_user_by_id(uuid).otp_hash

    def set_otp_hash(self, user_email: str, otp: str):
        """
        Set the otp hash value and the creation timestamp for telegram user confirmation
        
        Args:
            user_email: email of the requesting user
            otp: plain text of the otp
        Returns:
            the peewee User object. 
        """

        user = self.get_user_by_email(user_email)
        user.otp_hash = otp
        user.otp_created = datetime.now()
        user.save()
        return user

    def delete_otp_by_user(self, uuid) -> int:
        user = Users.get_by_id(uuid)

        log.error(f"user.otp_hash prima = {user.otp_hash}")

        user.otp_hash = None

        log.error(f"user.otp_hash dopo = {user.otp_hash}")

        return user.save()

    # Check user as verified
    def verify_user(self, uuid, telegram_user_id, telegram_user_name=None) -> int:
        user = Users.get_by_id(uuid)

        user.otp_hash = None
        user.telegram_user_id = telegram_user_id
        user.is_verified = True

        return user.save()
    
    # def get_community_group_by_id(self, uuid) -> CommunityGroups:
    #     return CommunityGroups.get_by_id(uuid)
    
    def get_all_community_groups(self) -> list:
        return CommunityGroups.select()
    
    def get_all_community_groups_by_departure_state(self, departure_state) -> list:
        return CommunityGroups.select().where(CommunityGroups.departure_state == departure_state)
        
    def get_community_groups_by_departure_state_and_arrival_city(self, departure_state, arrival_city):
        log.error(departure_state)

        try:
            return CommunityGroups.select(Groups.telegram_group_id).join(Groups).where(CommunityGroups.departure_state == departure_state, CommunityGroups.arrival_city == arrival_city)[0]
        except IndexError as e:
            log.error(e)
            return None
        
    def get_user_travel_list(self, uuid):
        return Travels.select(Travels).join(Users).where(Users.uuid == uuid)
    
    def create_new_travel_for_user(self, 
            user: str, 
            name_id: str, 
            travel_group: str, 
            departure_city: str, 
            arrival_city: str, 
            departure_date: str, 
            arrival_date: str, 
            trains_number: int, 
            trains: list) -> bool:
        user_uuid = Users.get_or_none(Users.telegram_user_id==user)
        travel = Travels.create(user_uuid, name_id, travel_group, departure_city, arrival_city, departure_date, arrival_date, trains_number)
        
        for train in trains:

            train_obj_list = Trains.select(Trains.uuid).join(TrainCompanies).join(DiscountProviders).where(DiscountProviders.name == train['train_company'], Trains.train_identifier == train['train_identifier'])
         
            if len(train_obj_list) == 1:
                l_travel_train = LTravelTrains.create(travel.uuid, train_obj_list[0].uuid, train.get('coach'), train.get('seat'))

                print("3")
                print(l_travel_train)

    def check_uni_domain(self, mail_domain):
        return UniDomains.select(UniDomains.uuid).where(UniDomains.name == mail_domain).exists()
    
    def check_memorandum(self, uni_domain):
        return Memorandum.select(Memorandum.uuid).where(Memorandum.uni_domain == uni_domain).exists()
        

    def check_active_discounts(self, email):
        # join tra Discount e User con filtro su User by email e su Discounts su is_used_soft a NULL
        return ((Discounts.select(Discounts.user).where(Discounts.is_used_soft.is_null(True))).join(Users, JOIN.INNER, on=(Users.uuid == Discounts.user)).where(Users.email == email)).count() <= 2 # TODO: use costants
    
    def check_city(self, city):
        return Cities.select().where(Cities.name == city) is not None
    
    def check_country(self, country):
        return Cities.select(Cities.country).where(Cities.country == country).exists()
    
    # def create_verification_token(self, user_to_verify):
    #     verification =  Verification(user = user_to_verify.uuid)
    #     verification.save()
        
    #     return verification
    
    def upsert_user_by_mail(self, email):
        return Users.get_or_create(
            email = email,
            uuid = uuid4()
        ) # return (user obj, created flag)


    def insert_travel_request(self,
        user_email, 
        user_uuid, 
        arrival_country,
        departure_country,
        travel_period,
        travel_requests,
        token=None):

        """
        Inserts travel requests after form submission.
        
        Args:
            user_email: email of the requesting user
            user_uuid: internal identifier of the user with that user_email
            arrival_country: arrival country specified by the requesting
            departure_country: departure countrey specified by the requester
            travel_request: the whole json request
            token: the token created to verify the email of the requesting user
        
        Returns:
            the peewee TravelRequest object. 
        """
        if token is None:
            token = uuid4()

        return TravelRequests.create(
            arrival_country = arrival_country, 
            departure_country = departure_country, 
            travel_period = travel_period, 
            travel_requests = travel_requests, 
            user_uuid = user_uuid, 
            user_mail = user_email, 
            uuid = uuid4(), 
            token = token)

    def get_user_by_otp_hash(self, token_hash: str):
        return Users.get(Users.otp_hash == token_hash)
        
    def delete_verification_link_token(self, user: Users):
        user.otp_hash = None
        user.otp_created = None
        user.save()
    
    def set_user_as_verified(self, user_telegram_id: str):
        """
        Set is_verified field of the user as the verification timestamp.
        
        Args:
            user_telegram_id: user telegram id for identification
        
        Returns:
            the peewee User object. 
        """
        user = self.get_user_by_telegram_id(telegram_id=user_telegram_id)
        user.is_verified = datetime.now()
        user.save()
        return user

    def insert_memorandum_request(self, 
        institution,
        email,
        uni_domain,
        requester_name,
        requester_surname,
        work_position,
        phone_number):
        """
        Inserts memorandum.
        
        Args:
            institution: institution that is doing request to access to Go2RAIL network
            email: email of who is doing the request
            uni_domain: university's email domain
            requester_name: name of the person who is doing request
            requester_surname: surname of the person who is doing request
            work_position: work position of the person who is doing request
            phone_number: phone number of the person who is doing request
        
        Returns:
            the peewee Memorandum object. 
        """

        return Memorandum.create(uuid= uuid4(), institution_name=institution, requester_mail=email, uni_domain=uni_domain,
            requester_name=requester_name,
            requester_surname=requester_surname,
            requester_work_position=work_position,
            requester_phone_number=phone_number)
    

    def get_memorandum(self, uuid):
        try:
            return Memorandum.get(Memorandum.uuid == uuid)
        except DoesNotExist as e:
            return None
        

    def set_memorandum_as_confirmed(self,  memorandum: Memorandum):
        memorandum.confirmed = datetime.now()
        memorandum.save()


    def insert_university(self, institution_name, memorandum_uuid):
        return Universities.create(name = institution_name, memorandum = memorandum_uuid)


    def insert_uni_domain(self, uni_domain, university_uuid):
        return UniDomains.create(name=uni_domain, university=university_uuid)
       

    def confirm_memorandum(self, memorandum):
        self.set_memorandum_as_confirmed(memorandum)
        # TODO insert della nuova città dove si trova l'università in base alla info del memorandum
        # forse converrebbe aggiungerla come descrizione
        university = self.insert_university(memorandum.institution_name, memorandum.uuid)
        self.insert_uni_domain(memorandum.uni_domain, university.uuid)

    def get_valid_otp_by_telegram_id(self, telegram_id):
        try:
            user = Users.get(Users.telegram_user_id == telegram_id)

            if not user.otp_created:
                raise DoesNotExist("No OTP available")
            
            if int((datetime.now() - user.otp_created).total_seconds()) // 60 > 10:
                raise ExpiredOtpException()
            
            return user.otp_hash
        except DoesNotExist as e:
            return None

    def get_otp_by_telegram_id(self, telegram_id):
        try:
            user = Users.get(Users.telegram_user_id == telegram_id)
            return user.otp_hash
        except DoesNotExist as e:
            return None
        
    def is_verified_user_by_telegram_id(self, telegram_id):
        user = Users.get(Users.telegram_user_id == telegram_id)
        if user.is_verified:
            return True
            
        return False
       