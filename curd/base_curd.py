# !/usr/bin/python3

# @Author: 花菜
# @File: base_curd.py
# @Time : 2022/9/4 17:45
# @Email: lihuacai168@gmail.com


from abc import ABC, abstractmethod
from typing import Any

from rest_framework.generics import get_object_or_404

from curd import crud_helper


class BaseCURD(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def create_obj(self, creator: str, payload: Any) -> int:
        ...

    @abstractmethod
    def get_obj_by_pk(self, pk: int) -> "obj":
        ...

    @abstractmethod
    def get_obj_by_unique_key(self, unique_key: dict) -> "obj":
        ...

    @abstractmethod
    def get_or_create(self, filter_kwargs: dict, defaults: dict) -> tuple["obj", bool]:
        ...

    @abstractmethod
    def list_obj(self, page_filter: dict) -> list[dict]:
        ...

    @abstractmethod
    def update_obj_by_pk(self, pk: int, updater: str, payload: dict) -> int:
        ...

    @abstractmethod
    def delete_obj_by_pk(self, pk: int) -> bool:
        ...


class GenericCURD(BaseCURD):
    def create_obj(self, creator: str, payload: Any) -> int:
        return crud_helper.create(creator, self.model, payload)

    def get_obj_by_pk(self, pk: int) -> "obj":
        return get_object_or_404(self.model, id=pk)

    def get_obj_by_unique_key(self, unique_key: dict) -> "obj":
        return get_object_or_404(self.model, **unique_key)

    def get_or_create(self, filter_kwargs: dict, defaults: dict) -> tuple["obj", bool]:
        return crud_helper.get_or_create(self.model, filter_kwargs, defaults)

    def list_obj(self, page_filter: dict) -> list[dict]:
        return self.model.objects.filter(**page_filter)

    def update_obj_by_pk(self, pk: int, updater: str, payload: dict) -> int:
        return crud_helper.update(self.get_obj_by_pk(pk), updater, payload)

    def delete_obj_by_pk(self, pk: int) -> bool:
        self.get_obj_by_pk(pk).delete()
        return True
