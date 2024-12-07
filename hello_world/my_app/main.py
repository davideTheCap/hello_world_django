from models.db import db
from models.person import Person
from repositories import PersonRepository

db.connect()
db.create_tables([Person])

person_repo = PersonRepository(Person)
person_repo.create(name="John", id=1)
person_repo.create(name="Bob", id=2)
employees = person_repo.all()
for employee in employees:
    print(employee.name)

db.close()
