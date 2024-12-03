from peewee import *
from playhouse.shortcuts import model_to_dict


def create_or_update(model_class, unique_fields, data):
    """
    Create or update a record in the database.

    :param model_class: The Peewee model class.
    :param unique_fields: List of field names to identify the record uniquely.
    :param data: Dictionary containing the fields and values for creation or update.
    :return: The created or updated model instance.
    """
    if not isinstance(unique_fields, (list, tuple)):
        raise ValueError("unique_fields must be a list or tuple of field names.")

    query = {field: data[field] for field in unique_fields}

    try:
        # Check if the record exists
        with model_class._meta.database.atomic():
            instance = model_class.get_or_none(**query)
            if instance:
                # Update existing record
                for key, value in data.items():
                    setattr(instance, key, value)
                instance.save()
            else:
                # Create new record
                instance = model_class.create(**data)
        return instance
    except IntegrityError as e:
        raise ValueError(f"Error creating or updating {model_class.__name__}: {e}")


db = SqliteDatabase('example.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db


class User(Model):
    username = CharField(unique=True)
    email = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([User, Person, Pet])

# Use create_or_update
user_data = {'username': 'johndoe', 'email': 'johndoe@example.com'}
user = create_or_update(User, ['username'], user_data)
print(model_to_dict(user))  # Output: {'id': 1, 'username': 'johndoe', 'email': 'johndoe@example.com'}

person_data = {'name': 'Gino', 'birthday': '22/09/1995'}
person = create_or_update(Person, [], person_data)
print(model_to_dict(person))
