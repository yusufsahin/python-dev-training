from dataclasses import dataclass


@dataclass
class DepartmentCreate:
    name: str


@dataclass
class DepartmentUpdate:
    name: str


@dataclass
class DepartmentRequest:
    name: str

    def to_create(self) -> DepartmentCreate:
        return DepartmentCreate(name=self.name)

    def to_update(self) -> DepartmentUpdate:
        return DepartmentUpdate(name=self.name)
