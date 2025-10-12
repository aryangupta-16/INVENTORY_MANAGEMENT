from fastapi import HTTPException, status

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

class UnauthorizedAccessError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")

class NotFoundError(HTTPException):
    def __init__(self, entity: str = "Resource"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} not found")

class ConflictError(HTTPException):
    def __init__(self, entity: str = "Resource"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"{entity} already exists")

class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)

class VectorIndexError(HTTPException):
    def __init__(self, message: str = "Error while updating vector index"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)

class InternalServerError(HTTPException):
    def __init__(self, message: str = "An unexpected error occurred"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
