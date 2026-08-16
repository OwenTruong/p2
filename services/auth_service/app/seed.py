from app.services.auth_service import AuthService
from app.dtos.user_dto import UserCreateRequestDTO


SEED_USERS = [
    UserCreateRequestDTO(
        email="admin@gmail.com",
        password="password123",
        first_name="Admin",
        last_name="SpaceBnB",
    ),
    UserCreateRequestDTO(
        email="john@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    ),
]

def seed_users() -> None:
    service = AuthService()

    for dto in SEED_USERS:
        try:
            service.save_user(dto)
            print(f"Created seed user: {dto.email}")
        except Exception as exc:
            print(f"Skipped {dto.email}: {exc}")


if __name__ == "__main__":
    seed_users()