from fastapi import APIRouter, Depends, status, HTTPException
from app.dtos.listing import ListingCreateRequestDTO, ListingResponseDTO
from app.services.listing_service import ListingService
from shared.dependencies.auth import get_current_user
from shared.dtos.auth_user import AuthenticatedUser
from shared.utils.exceptions import ActiveReservationException, NoFetchedResultException, UserDoesNotOwnException

router = APIRouter(prefix="/api/listings", tags=["Listings"])
listing_service = ListingService()

@router.post("", response_model=ListingResponseDTO, status_code=status.HTTP_201_CREATED)
def create_listing(
    dto: ListingCreateRequestDTO,
    # current_user: AuthenticatedUser = Depends(get_current_user)
):
    created_listing = listing_service.create_listing(
        host_id=1, 
        dto=dto
    )
    
    return ListingResponseDTO.model_validate(created_listing)

@router.delete("/{listing_id}", status_code=status.HTTP_200_OK)
def delete_listing(
    listing_id: int,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        listing_service.delete_listing(current_user.user_id, listing_id)
    except UserDoesNotOwnException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {
            "errors": [
                {
                    "message": "User does not own the listing."
                }
            ]
        })
    except ActiveReservationException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {
            "errors": [
                {
                    "message": "Listing does not exist."
                }
            ]
        })
    except NoFetchedResultException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, {
            "errors": [
                {
                    "message": "Listing maybe not be removed due to an active reservation."
                }
            ]
        })
