from typing import Generic, List, Optional

from peewee import DoesNotExist

from my_app.models.T import T


class GenericRepository(Generic[T]):
    def __init__(self, model: T):
        self.model = model

    def create(self, **kwargs) -> T:
        return self.model.create(**kwargs)

    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.model.get_by_id(id)
        except DoesNotExist:
            return None

    def update(self, instance: T, **kwargs) -> bool:
        query = self.model.update(**kwargs).where(self.model.id == instance.id)
        return query.execute() > 0

    def delete(self, instance: T) -> bool:
        return instance.delete_instance() > 0

    def all(self) -> List[T]:
        return list(self.model.select())

    def filter(self, **kwargs) -> List[T]:
        return list(self.model.filter(**kwargs))
