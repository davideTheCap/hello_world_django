# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class BaseModel(peewee.Model):
    
    class Meta:
        table_name = "basemodel"


@snapshot.append
class Cities(peewee.Model):
    uuid = AutoField(primary_key=True)
    country = CharField(max_length=255)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    name = CharField(max_length=255)
    class Meta:
        table_name = "cities"


@snapshot.append
class ChatGroups(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    arrival_city = snapshot.ForeignKeyField(column_name='arrival_city', index=True, model='cities', null=True)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    departure_city = snapshot.ForeignKeyField(backref='cities_departure_city_set', column_name='departure_city', index=True, model='cities', null=True)
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    name = CharField(max_length=255, null=True)
    telegram_group_id = IntegerField()
    telegram_invite_link = CharField(max_length=255, null=True)
    class Meta:
        table_name = "chat_groups"


@snapshot.append
class DiscountProviders(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    name = CharField(max_length=255)
    class Meta:
        table_name = "discount_providers"


@snapshot.append
class Users(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    email = CharField(max_length=100, unique=True)
    is_verified = DateTimeField(null=True)
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    otp_created = DateTimeField(null=True)
    otp_hash = CharField(max_length=255, null=True)
    telegram_user_id = IntegerField(null=True, unique=True)
    telegram_username = CharField(max_length=255, null=True, unique=True)
    class Meta:
        table_name = "users"


@snapshot.append
class Discounts(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    discount_code = CharField(max_length=255)
    discount_provider = snapshot.ForeignKeyField(column_name='discount_provider', index=True, model='discountproviders')
    discount_rate = FloatField()
    is_used_hard = DateTimeField(null=True)
    is_used_soft = DateTimeField(null=True)
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    user = snapshot.ForeignKeyField(column_name='user', index=True, model='users', null=True)
    user_delivery_date = DateTimeField(null=True)
    validity_begin = DateTimeField(null=True)
    validity_end = DateTimeField(null=True)
    class Meta:
        table_name = "discounts"


@snapshot.append
class LUsersGroups(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    chat_group = snapshot.ForeignKeyField(column_name='chat_group', index=True, model='chatgroups')
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    user = snapshot.ForeignKeyField(column_name='user', index=True, model='users')
    class Meta:
        table_name = "l_users_groups"
        indexes = (
            (('user', 'chat_group'), True),
            )


@snapshot.append
class Memorandum(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    confirmed = DateTimeField()
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    institution_name = CharField(max_length=255)
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    requester_mail = CharField(max_length=255)
    requester_name = CharField(max_length=255)
    requester_phone_number = CharField(max_length=255)
    requester_surname = CharField(max_length=255)
    requester_work_position = CharField(max_length=255)
    uni_domain = CharField(max_length=255)
    class Meta:
        table_name = "memorandum"


@snapshot.append
class Topics(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    chat_group = snapshot.ForeignKeyField(column_name='chat_group', index=True, model='chatgroups', null=True)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    name = CharField(max_length=255, null=True)
    telegram_thread_id = IntegerField(null=True)
    class Meta:
        table_name = "topics"


@snapshot.append
class TravelRequests(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    arrival_country = CharField(max_length=255)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], null=True)
    departure_country = CharField(max_length=255)
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], null=True)
    travel_period = DateTimeField()
    user = snapshot.ForeignKeyField(column_name='user', index=True, model='users')
    user_mail = CharField(max_length=255)
    class Meta:
        table_name = "travel_requests"


@snapshot.append
class Travels(peewee.Model):
    uuid = CharField(max_length=255, primary_key=True)
    arrival_city = snapshot.ForeignKeyField(column_name='arrival_city', index=True, model='cities')
    arrival_date = DateTimeField()
    chat_group = snapshot.ForeignKeyField(column_name='chat_group', index=True, model='chatgroups')
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], null=True)
    departure_city = snapshot.ForeignKeyField(backref='cities_departure_city_set', column_name='departure_city', index=True, model='cities')
    departure_date = DateTimeField()
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], null=True)
    travel_request = snapshot.ForeignKeyField(column_name='travel_request', index=True, model='travelrequests')
    user = snapshot.ForeignKeyField(column_name='user', index=True, model='users')
    class Meta:
        table_name = "travels"


@snapshot.append
class TrainDiscounts(peewee.Model):
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    discount = snapshot.ForeignKeyField(column_name='discount', index=True, model='discounts')
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    max_uses_numbers = IntegerField()
    territory = CharField(max_length=255, null=True)
    travel = snapshot.ForeignKeyField(column_name='travel', index=True, model='travels', null=True)
    travel_time_range_begin = DateTimeField(null=True)
    travel_time_range_end = DateTimeField(null=True)
    uuid = CharField(max_length=255)
    class Meta:
        table_name = "train_discounts"
        primary_key = False


@snapshot.append
class Universities(peewee.Model):
    uuid = AutoField(primary_key=True)
    city = snapshot.ForeignKeyField(column_name='city', index=True, model='cities')
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    memorandum = snapshot.ForeignKeyField(column_name='memorandum', index=True, model='memorandum')
    name = CharField(max_length=255)
    uni_domain = CharField(max_length=255)
    class Meta:
        table_name = "universities"


@snapshot.append
class UniDomains(peewee.Model):
    uuid = AutoField(primary_key=True)
    name = CharField(max_length=80)
    created = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    last_updated = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    university = snapshot.ForeignKeyField(column_name='university', index=True, model='universities')
    class Meta:
        table_name = "uni_domains"


