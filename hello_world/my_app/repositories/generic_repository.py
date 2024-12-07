# TODO: idea con valerio
# abstract class base_interface(): <T> {
#     find_by_id(uuid: string): <T>
#     delete_by_id(uuid: string): void
#     create_or_update(<T> obj): <T>
#     update(<T>): <T> --> maybe provided by peewe (find + create_or_update()?)
# }

# Define type variables
from typing import *

T = TypeVar('T')


class GenericRepository(Generic[T]):
    def __init__(self):
        self.items: List[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get(self, id: int) -> Optional[T]:
        return next((item for item in self.items if getattr(item, 'id', None) == id), None)

    def update(self, item: T) -> None:
        for i, existing_item in enumerate(self.items):
            if getattr(existing_item, 'id', None) == getattr(item, 'id', None):
                self.items[i] = item
                break

    def delete(self, id: int) -> None:
        self.items = [item for item in self.items if getattr(item, 'id', None) != id]

    def all(self) -> List[T]:
        return self.items
