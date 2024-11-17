import datetime
from peewee import *

db = MySQLDatabase(
    'go2rail',
    charset = "utf8mb4",
    sql_mode = "PIPES_AS_CONCAT",
    use_unicode = True,
    host = '127.0.0.1',
    port = int('3304'),
    user = 'go2rail',
    password = 'password'
)

class Foo(db.Model):
    bar = CharField(max_length=50)
    baz = IntegerField()
    quux = IntegerField()

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)

class Tweet(BaseModel):
    user = ForeignKeyField(User, backref='tweets')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)


MODELS = [Tweet, User, BaseModel]
for model in MODELS:
    model.bind(db, bind_refs=False, bind_backrefs=False)