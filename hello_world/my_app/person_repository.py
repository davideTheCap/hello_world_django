from my_app.generic_repository import *
from my_app.person import *


class PersonRepository(GenericRepository[Person]):
    def __init__(self: [Person]):
        super().__init__()