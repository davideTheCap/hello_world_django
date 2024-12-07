from my_app.person import *
from my_app.person_repository import PersonRepository

# from playhouse.shortcuts import model_to_dict

emp = Person("Satyam", 102)  # An Object of Person
emp.Display()
person_repo = PersonRepository()
person_repo.add(emp)
