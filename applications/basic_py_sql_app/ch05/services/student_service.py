from db.dialect import SqlDialect
from db.schema import create_table
from db.seed import seed_data
from dto.student_dto import StudentRequest
from ports import ConnectionFactory, StudentRepository


class StudentService:
    def __init__(
        self,
        repository: StudentRepository,
        connect: ConnectionFactory,
        dialect: SqlDialect,
    ) -> None:
        self._repository = repository
        self._connect = connect
        self._dialect = dialect

    def initialize_app(self) -> None:
        create_table(self._connect, self._dialect)

    def load_seed_data(self) -> int:
        return seed_data(self._connect, self._dialect)

    def get_students(self):
        return self._repository.list_students()

    def get_student(self, student_id: int):
        return self._repository.get_student_by_id(student_id)

    def add_student(self, student_request: StudentRequest) -> bool:
        return self._repository.insert_student(student_request.to_create())

    def edit_student(self, student_id: int, student_request: StudentRequest) -> bool:
        return self._repository.update_student(student_id, student_request.to_update())

    def remove_student(self, student_id: int) -> bool:
        return self._repository.delete_student(student_id)
