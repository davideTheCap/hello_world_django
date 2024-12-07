from peewee import CharField, IntegerField

from my_app.repositories.person_repository import PersonRepository
from .base_models import BaseModel


class Person(BaseModel):
    name = CharField()
    id = IntegerField()

    class Meta:
        table_name = "product"

    # Display method inside the class
    def display(self):
        print(self.name, self.id)


person_repo = PersonRepository()
person_repo.add(Person("John", 1))
person_repo.add(Person("Bob", 2))
employees = person_repo.all()
for employee in employees:
    print(employee.name)
