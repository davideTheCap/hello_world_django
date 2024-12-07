from peewee import CharField, IntegerField

from .base_models import BaseModel


class Person(BaseModel):
    name = CharField()
    id = IntegerField()

    class Meta:
        table_name = "person"

    # Display method inside the class
    def display(self):
        print(self.name, self.id)
