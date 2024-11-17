from peewee import *
import os

from dotenv import load_dotenv
load_dotenv()

model_database = MySQLDatabase(
    'go2rail',
    charset = "utf8mb4",
    sql_mode = "PIPES_AS_CONCAT",
    use_unicode = True,
    host = '127.0.0.1',
    port = int(3304),
    user = 'go2rail',
    password = 'password'
)


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = model_database


class Cities(BaseModel):
    country = CharField()
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    name = CharField()
    uuid = AutoField()

    class Meta:
        table_name = "cities"


class ChatGroups(BaseModel):
    arrival_city = ForeignKeyField(
        column_name="arrival_city", field="uuid", model=Cities, null=True
    )
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    departure_city = ForeignKeyField(
        backref="cities_departure_city_set",
        column_name="departure_city",
        field="uuid",
        model=Cities,
        null=True,
    )
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    name = CharField(null=True)
    telegram_group_id = IntegerField()
    telegram_invite_link = CharField(null=True)
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "chat_groups"


class DiscountProviders(BaseModel):
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    name = CharField()
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "discount_providers"


class Users(BaseModel):
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    email = CharField(unique=True, max_length=100)
    is_verified = DateTimeField(null=True)
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    otp_created = DateTimeField(null=True)
    otp_hash = CharField(null=True)
    telegram_user_id = IntegerField(null=True, unique=True)
    telegram_username = CharField(null=True, unique=True)
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "users"


class Discounts(BaseModel):
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    discount_code = CharField()
    discount_provider = ForeignKeyField(
        column_name="discount_provider", field="uuid", model=DiscountProviders
    )
    discount_rate = FloatField()
    is_used_hard = DateTimeField(null=True)
    is_used_soft = DateTimeField(null=True)
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    user = ForeignKeyField(column_name="user", field="uuid", model=Users, null=True)
    user_delivery_date = DateTimeField(null=True)
    uuid = CharField(primary_key=True)
    validity_begin = DateTimeField(null=True)
    validity_end = DateTimeField(null=True)

    class Meta:
        table_name = "discounts"


class Memorandum(BaseModel):
    confirmed = DateTimeField()
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    institution_name = CharField()
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    requester_mail = CharField()
    requester_name = CharField()
    requester_phone_number = CharField()
    requester_surname = CharField()
    requester_work_position = CharField()
    uni_domain = CharField()
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "memorandum"


# class Universities(BaseModel):
#     city = ForeignKeyField(column_name="city", field="uuid", model=Cities)
#     created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
#     last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
#     memorandum = ForeignKeyField(
#         column_name="memorandum", field="uuid", model=Memorandum
#     )
#     name = CharField()
#     uuid = AutoField()

#     class Meta:
#         table_name = "universities"


# class Domains(BaseModel):
#     created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
#     domain = CharField()
#     last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
#     university = ForeignKeyField(
#         column_name="university", field="uuid", model=Universities
#     )
#     uuid = AutoField()

#     class Meta:
#         table_name = "domains"


class LUsersGroups(BaseModel):
    chat_group = ForeignKeyField(
        column_name="chat_group", field="uuid", model=ChatGroups
    )
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    user = ForeignKeyField(column_name="user", field="uuid", model=Users)
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "l_users_groups"
        indexes = ((("user", "chat_group"), True),)


class Topics(BaseModel):
    chat_group = ForeignKeyField(
        column_name="chat_group", field="uuid", model=ChatGroups, null=True
    )
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    name = CharField(null=True)
    telegram_thread_id = IntegerField(null=True)
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "topics"


class TravelRequests(BaseModel):
    arrival_country = CharField()
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    departure_country = CharField()
    last_updated = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True
    )
    travel_period = DateTimeField()
    travel_requests = UnknownField(null=True)  # json
    user = ForeignKeyField(column_name="user", field="uuid", model=Users)
    user_mail = CharField()
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "travel_requests"


class Travels(BaseModel):
    arrival_city = ForeignKeyField(
        column_name="arrival_city", field="uuid", model=Cities
    )
    arrival_date = DateTimeField()
    chat_group = ForeignKeyField(
        column_name="chat_group", field="uuid", model=ChatGroups
    )
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    departure_city = ForeignKeyField(
        backref="cities_departure_city_set",
        column_name="departure_city",
        field="uuid",
        model=Cities,
    )
    departure_date = DateTimeField()
    last_updated = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True
    )
    travel_request = ForeignKeyField(
        column_name="travel_request", field="uuid", model=TravelRequests
    )
    user = ForeignKeyField(column_name="user", field="uuid", model=Users)
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = "travels"


class TrainDiscounts(BaseModel):
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    discount = ForeignKeyField(column_name="discount", field="uuid", model=Discounts)
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    max_uses_numbers = IntegerField()
    territory = CharField(null=True)
    travel = ForeignKeyField(
        column_name="travel", field="uuid", model=Travels, null=True
    )
    travel_time_range_begin = DateTimeField(null=True)
    travel_time_range_end = DateTimeField(null=True)
    uuid = CharField()

    class Meta:
        table_name = "train_discounts"
        primary_key = False


class Universities(BaseModel):
    city = ForeignKeyField(column_name="city", field="uuid", model=Cities)
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    memorandum = ForeignKeyField(
        column_name="memorandum", field="uuid", model=Memorandum
    )
    name = CharField()
    uni_domain = CharField()
    uuid = AutoField(primary_key=True)

    class Meta:
        table_name = "universities"


class UniDomains(Model):
    
    uuid = AutoField(primary_key=True)
    name = CharField(80)
    university = IntegerField()
    created = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_updated = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    university = ForeignKeyField(
        column_name="university", field="uuid", model=Universities, null=False
    )

    class Meta:
        table_name = "uni_domains"



MODELS = [UniDomains, Universities, TrainDiscounts, Travels, TravelRequests, Topics, LUsersGroups, Memorandum, Discounts, Users, DiscountProviders, ChatGroups, Cities]
for model in MODELS:
    model.bind(model_database, bind_refs=False, bind_backrefs=False)