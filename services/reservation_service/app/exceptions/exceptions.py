from shared.dtos.errors import ApiErrorDTO
from shared.exceptions.exceptions import ApiException


class InvalidReservationDateRangeException(ApiException):
    def __init__(self):
        super().__init__(
            400,
            [
                ApiErrorDTO(
                    message="Check-out date must be after check-in date."
                )
            ],
        )


class ReservationAccessForbiddenException(ApiException):
    def __init__(self):
        super().__init__(
            403,
            [
                ApiErrorDTO(
                    message="You are not authorized to access this reservation."
                )
            ],
        )


class GuestOwnsListingException(ApiException):
    def __init__(self):
        super().__init__(
            403,
            [
                ApiErrorDTO(
                    message="A host cannot reserve their own listing."
                )
            ],
        )


class ReservationDateConflictException(ApiException):
    def __init__(self):
        super().__init__(
            409,
            [
                ApiErrorDTO(
                    message="The requested dates overlap an existing reservation."
                )
            ],
        )


class ReservationAlreadyCancelledException(ApiException):
    def __init__(self):
        super().__init__(
            409,
            [
                ApiErrorDTO(
                    message="Reservation is already cancelled."
                )
            ],
        )


class ReservationCancellationNotAllowedException(ApiException):
    def __init__(self):
        super().__init__(
            409,
            [
                ApiErrorDTO(
                    message="Reservation cannot be cancelled on or after check-in."
                )
            ],
        )