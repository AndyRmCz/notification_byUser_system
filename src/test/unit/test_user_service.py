import pytest
from src.modules.users.models import User
from src.modules.users.schemas import UserRegisterRequest, UserLoginRequest
from src.modules.users.repositories import IUserRepository
from src.modules.users.services import UserService
from src.modules.users.exceptions import UserAlreadyExistsError, InvalidCredentialsError

class FakeUserRepository(IUserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}

    async def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._users.values() if u.email == email), None)
    
    async def get_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)
    
    async def create(self, user: User) -> User:
        user.id = f"uuid-{len(self._users) + 1}"
        self._users[user.id] = user
        return user
    
@pytest.mark.asyncio
async def test_register_user_success():
    repo = FakeUserRepository()
    service = UserService(repo)
    dto = UserRegisterRequest(email="new@user.com", password="password123")

    result = await service.register_user(dto)

    assert result.email == "new@user.com"
    assert result.id is not None

@pytest.mark.asyncio
async def test_register_duplicate_user_raises_exception():
    repo = FakeUserRepository()
    service = UserService(repo)
    dto = UserRegisterRequest(email="dup@user.com", password="password123")
    await service.register_user(dto)

    with pytest.raises(UserAlreadyExistsError):
        await service.register_user(dto)