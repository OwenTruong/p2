from datetime import date
from decimal import Decimal

from fastapi import Depends

from app.models.reservation import Reservation, ReservationStatus
from ..dtos.listing import ListingResponseDTO
from ..dtos.reservation import CreateReservationRequest, CreateReservationResponse, ReservationResponse
from ..repositories.reservation_repository import ReservationRepository
from ..clients.listing_client import ListingClient
from shared.exceptions.exceptions import ListingNotFoundException, ListingUnavailableException, ReservationNotFoundException
from ..exceptions.exceptions import GuestOwnsListingException, InvalidReservationDateRangeException, ReservationAccessForbiddenException, ReservationAlreadyCancelledException, ReservationCancellationNotAllowedException, ReservationDateConflictException


class ReservationService:
    def __init__(
        self,
        reservation_repository : ReservationRepository,
        listing_client : ListingClient
    ):
        self.reservation_repository = reservation_repository
        self.listing_client = listing_client

    def create(
        self,
        guest_id: int,
        request: CreateReservationRequest
    ) -> CreateReservationResponse:

        listing_id = request.listing_id
        check_in_date = request.check_in_date
        check_out_date = request.check_out_date
        
        if check_out_date <= check_in_date:
            raise InvalidReservationDateRangeException()

        listing_data = self.listing_client.find_by_id(listing_id)

        if listing_data is None:
            raise ListingNotFoundException()

        listing = ListingResponseDTO.model_validate(listing_data)

        if listing.host_id == guest_id:
            raise GuestOwnsListingException()

        if not listing.is_published:
            raise ListingUnavailableException()

        existing = (
            self.reservation_repository.find_all_by_listing_id(
                listing_id,
                status=ReservationStatus.ACCEPTED,
            )
        )

        for reservation in existing:
            overlaps = (
                reservation.check_in_date < check_out_date
                and
                reservation.check_out_date > check_in_date
            )

            if overlaps:
                raise ReservationDateConflictException()

        number_of_nights = (
            check_out_date - check_in_date
        ).days

        total_price = (
            listing.price_per_night
            * Decimal(number_of_nights)
        )

        reservation = Reservation(
            listing_id=listing_id,
            guest_id=guest_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price,
        )

        return self.reservation_repository.save(reservation)

    def find_for_guest(
        self,
        guest_id: int,
        status: ReservationStatus | None = None,
    ) -> list[ReservationResponse]:

        reservations = self.reservation_repository.find_all_by_guest_id(
            guest_id,
            status,
        )

        return [ReservationResponse(
            reservation_id=reservation.reservation_id,
            listing_id=reservation.listing_id,
            guest_id=reservation.guest_id,
            check_in_date=reservation.check_in_date,
            check_out_date=reservation.check_out_date,
            total_price=reservation.total_price,
            status=reservation.status,
        )
            for reservation in reservations
        ]

    def find_by_id(
        self,
        reservation_id: int,
        current_user_id: int,
    ) -> Reservation:

        reservation = self.reservation_repository.find_by_id(reservation_id)

        if reservation is None:
            raise ReservationNotFoundException()

        listing = ListingResponseDTO.model_validate(self.listing_client.find_by_id(reservation.listing_id))

        is_guest = (reservation.guest_id == current_user_id)
        is_host = (listing.host_id == current_user_id)

        if not is_guest and not is_host:
            raise ReservationAccessForbiddenException()

        return reservation

    def update(
        self,
        reservation_id: int,
        current_user_id: int,
        check_in_date: date,
        check_out_date: date,
    ) -> Reservation:

        reservation = self.reservation_repository.find_by_id(reservation_id)

        if reservation is None:
            raise ReservationNotFoundException()

        if reservation.guest_id != current_user_id:
            raise ReservationAccessForbiddenException()

        if check_out_date <= check_in_date:
            raise InvalidReservationDateRangeException()

        existing = self.reservation_repository.find_all_by_listing_id(
                reservation.listing_id,
                status=ReservationStatus.ACCEPTED,
            )

        for other in existing:

            if (other.reservation_id == reservation.reservation_id):
                continue

            overlaps = (
                other.check_in_date < check_out_date
                and
                other.check_out_date > check_in_date
            )

            if overlaps:
                raise ReservationDateConflictException()

        listing = ListingResponseDTO.model_validate(self.listing_client.find_by_id(reservation.listing_id))

        nights = (check_out_date - check_in_date).days

        reservation.check_in_date = check_in_date
        reservation.check_out_date = check_out_date
        reservation.total_price = listing.price_per_night * Decimal(nights)

        return self.reservation_repository.update(reservation)

    def cancel(
        self,
        reservation_id: int,
        current_user_id: int,
    ) -> None:

        reservation = self.reservation_repository.find_by_id(reservation_id)

        if reservation is None:
            raise ReservationNotFoundException()

        if reservation.guest_id != current_user_id:
            raise ReservationAccessForbiddenException()

        if (reservation.status == ReservationStatus.CANCELLED):
            raise ReservationAlreadyCancelledException()

        if date.today() >= reservation.check_in_date:
            raise ReservationCancellationNotAllowedException()

        self.reservation_repository.cancel(reservation_id)

    def find_for_listing(
        self,
        listing_id: int,
        status: ReservationStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[ReservationResponse]:

        reservations = self.reservation_repository.find_all_by_listing_id(
                    listing_id=listing_id,
                    status=status,
                    start_date=start_date,
                    end_date=end_date,
                )

        return [ReservationResponse(
                reservation_id=reservation.reservation_id,
                listing_id=reservation.listing_id,
                guest_id=reservation.guest_id,
                check_in_date=reservation.check_in_date,
                check_out_date=reservation.check_out_date,
                total_price=reservation.total_price,
                status=reservation.status, 
            )
            for reservation in reservations
        ]
        