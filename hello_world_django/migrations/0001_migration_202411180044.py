# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Foo(peewee.Model):
    bar = CharField(max_length=50)
    baz = IntegerField()
    quux = IntegerField()
    class Meta:
        table_name = "foo"


