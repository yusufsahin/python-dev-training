from typing import Generic, Optional, TypeVar

from django.db import models as django_models

T = TypeVar("T", bound=django_models.Model)


class BaseRepository(Generic[T]):
    model_class: type[T]

    def get_by_id(self, pk: int) -> Optional[T]:
        try:
            return self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return None

    def get_all(self) -> django_models.QuerySet[T]:
        return self.model_class.objects.all()

    def save(self, instance: T) -> T:
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()
