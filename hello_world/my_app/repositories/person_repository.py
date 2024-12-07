from my_app.models.T import T
from .generic_repository import GenericRepository


class PersonRepository(GenericRepository[T]):
    def __init__(self):
        super().__init__()