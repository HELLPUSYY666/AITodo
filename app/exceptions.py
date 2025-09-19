from typing import Any, Dict, cast

from fastapi import HTTPException, status
from httpx import Headers


class BaseServiceException(HTTPException):
    pass


class Unauthorized(BaseServiceException):
    def __init__(self, headers: Dict[str, Any] | Headers | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers=cast(dict[str, Any], headers),
        )


class AlreadyExists(BaseServiceException):
    def __init__(
        self, model_name: str, headers: Dict[str, Any] | Headers | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{model_name.capitalize()} already exists",
            headers=cast(dict[str, Any], headers),
        )


class NotFound(BaseServiceException):
    def __init__(
        self,
        model_name: str,
        ident: int,
        headers: Dict[str, Any] | Headers | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name.capitalize()} with ident: {ident} not found",
            headers=cast(dict[str, Any], headers),
        )


class NotNullViolation(BaseServiceException):
    def __init__(
        self, detail: str, headers: Dict[str, Any] | Headers | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=cast(dict[str, Any], headers),
        )
