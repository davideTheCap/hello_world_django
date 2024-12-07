from my_app.person import *
from my_app.person_repository import PersonRepository

person_repo = PersonRepository()
person_repo.add(Person("John", 1))
person_repo.add(Person("Bob", 2))

employees = person_repo.all()
for employee in employees:
    print(employee.name)
