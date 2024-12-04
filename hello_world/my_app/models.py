from peewee import *

from my_app.db_interface import *
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('people.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.connect()
db.create_tables([Person, Pet])

from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save() # bob is now stored in the database
# Returns: 1

grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

grandma.name = 'Grandma L.'
grandma.save()  # Update grandma's name in the database.
# Returns: 1

bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

herb_mittens.delete_instance() # he had a great life
# Returns: 1

herb_fido.owner = uncle_bob
herb_fido.save()


# retrieving data
grandma = Person.select().where(Person.name == 'Grandma L.').get()
grandma = Person.get(Person.name == 'Grandma L.')


# for person in Person.select():
#     print(person.name)

# prints:
# Bob
# Grandma L.
# Herb


query = Pet.select().where(Pet.animal_type == 'cat')
# for pet in query:
#     print(pet.name, pet.owner.name)

# prints:
# Kitty Bob
# Mittens Jr Herb

query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

# for pet in query:
#     print(pet.name, pet.owner.name)

# prints:
# Kitty Bob
# Mittens Jr Herb

# Create or Update
person_data = {'name': 'Gino', 'birthday': '22/09/1995'}
person = create_or_update(Person, [], person_data)
print(person)

# Find by Id
person_found = find_by_id(Person, 1)
if person_found:
    print(f"Person found: {person_found.name}, {person_found.birthday}")
else:
    print("Person not found.")

# Find all
persons = find_all(Person)
for person in persons:
    print(person.name, person.birthday)