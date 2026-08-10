from pydantic import BaseModel

# Describe one client-facing error
# ApiErrorDTO evolves according to how clients need to understand individual errors.
class ApiErrorDTO(BaseModel):
    message: str

# Define complete HTTP error body
# ApiErrorResponseDTO evolves according to the overall API error contract.
class ApiErrorResponseDTO(BaseModel):
    errors: list[ApiErrorDTO]

