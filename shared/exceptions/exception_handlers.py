from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from shared.dtos.errors import ApiErrorDTO, ApiErrorResponseDTO
from shared.exceptions.exceptions import ApiException, EmailAlreadyExistsException

def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content=ApiErrorResponseDTO(
                errors=[
                    ApiErrorDTO(
                        message="An unexpected error occurred."
                    )
                ]
            ).model_dump(),
        )

    @app.exception_handler(ApiException)
    async def api_exception_handler(
        request: Request,
        exc: ApiException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiErrorResponseDTO(
                errors=exc.errors
            ).model_dump(),
        )

    # Pydantic validation should serve as a trust boundary for backend processing
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):

        print(exc)
        
        return JSONResponse(
            status_code=422, 
            content=ApiErrorResponseDTO(
                errors=[
                    ApiErrorDTO(
                        message="Invalid inputs."
                    )
                ]
            ).model_dump()
        )