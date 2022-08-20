from http import HTTPStatus
from typing import Any


class AppError(Exception):

    def __init__(self, reason: str, status: HTTPStatus) -> None:
        super().__init__(reason)
        self.status = status
        self.reason = reason


class NotFoundError(AppError):
    status = HTTPStatus.NOT_FOUND

    def __init__(self, entity: str, uid: Any) -> None:
        super().__init__(
            reason=f'Not found {entity} [{uid}]',
            status=self.status,
        )
        self.entity = entity
        self.uid = uid


class AlreadyExistsError(AppError):
    status = HTTPStatus.CONFLICT

    def __init__(self, entity: str, constraint: str) -> None:
        super().__init__(
            reason=f'{entity}: constraint violation',
            status=self.status,
        )
        self.entity = entity
        self.constraint = constraint
