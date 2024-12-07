from typing import TypeVar, Generic, List, Optional

from peewee import Model

# TODO: idea con valerio
# abstract class base_interface(): <T> {
#     find_by_id(uuid: string): <T>
#     delete_by_id(uuid: string): void
#     create_or_update(<T> obj): <T>
#     update(<T>): <T> --> maybe provided by peewe (find + create_or_update()?)
# }

# Define type variables
T = TypeVar('T', bound=Model)


class BaseRepository(Generic[T]):
    def __init__(self, model: T):
        self.model = model

    def create(self, **kwargs) -> T:
        return self.model.create(**kwargs)

    def get(self, id: int) -> Optional[T]:
        return self.model.get_or_none(self.model.id == id)

    def update(self, id: int, **kwargs) -> int:
        query = self.model.update(**kwargs).where(self.model.id == id)
        return query.execute()

    def delete(self, id: int) -> int:
        query = self.model.delete().where(self.model.id == id)
        return query.execute()

    def all(self) -> List[T]:
        return list(self.model.select())
