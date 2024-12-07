from models.person import *
from repositories.generic_repository import *


class PersonRepository(GenericRepository[Person]):
    def __init__(self):
        super().__init__()