
from shared.dtos.errors import ApiErrorDTO

# Carry failure through application
# ApiException evolves according to application error-handling needs.
class ApiException(Exception):
    def __init__(self, status_code: int, errors: list[ApiErrorDTO]):
        super().__init__(errors[0].message if errors else "API error")
        self.status_code = status_code
        self.errors = errors

class UnauthorizedException(ApiException):
    def __init__(self, message: str = "Missing or invalid authentication credentials."):
        super().__init__(401, [ApiErrorDTO(message=message)])

class ForbiddenException(ApiException):
    def __init__(self, message: str = "Forbidden resource access."):
        super().__init__(403, [ApiErrorDTO(message=message)])

class NotFoundException(ApiException):
    def __init__(self, message: str = "Resource not found."):
        super().__init__(404, [ApiErrorDTO(message=message)])

class EmailAlreadyExistsException(ApiException):
    def __init__(self):
        super().__init__(409, [ApiErrorDTO(message="User with this email already exists.")])    
        
