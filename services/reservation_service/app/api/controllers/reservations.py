
from fastapi import APIRouter, Depends, status

from ...di.dependency_injection import get_reservation_service
from ...models.reservation import ReservationStatus
from ...dtos.reservation import CreateReservationRequest, UpdateReservationRequest, CreateReservationResponse
from shared.dependencies.auth import get_current_user


router = APIRouter(prefix="/api/reservations", tags=["reservations"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_reservation(
    request: CreateReservationRequest,
    current_user=Depends(get_current_user),
    service=Depends(get_reservation_service),
) -> CreateReservationResponse:
    return service.create(
        guest_id=current_user.user_id,
        request=request
    )

@router.get("/me")
def get_my_reservations(
    status: ReservationStatus | None = None,
    current_user=Depends(get_current_user),
    service=Depends(get_reservation_service),
):
    return service.find_for_guest(
        guest_id=current_user.user_id,
        status=status,
    )

@router.get("/{reservation_id}")
def get_reservation(
    reservation_id: int,
    current_user=Depends(get_current_user),
    service=Depends(get_reservation_service),
):
    return service.find_by_id(
        reservation_id,
        current_user.user_id,
    )

@router.put("/{reservation_id}")
def update_reservation(
    reservation_id: int,
    request: UpdateReservationRequest,
    current_user=Depends(get_current_user),
    service=Depends(get_reservation_service),
):
    return service.update(
        reservation_id=reservation_id,
        current_user_id=current_user.user_id,
        check_in_date=request.check_in_date,
        check_out_date=request.check_out_date,
    )

@router.delete("/{reservation_id}",status_code=status.HTTP_204_NO_CONTENT,)
def cancel_reservation(
    reservation_id: int,
    current_user=Depends(get_current_user),
    service=Depends(get_reservation_service),
):
    service.cancel(reservation_id, current_user.user_id)