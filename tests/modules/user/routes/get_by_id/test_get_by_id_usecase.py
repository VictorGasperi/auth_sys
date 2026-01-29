import pytest
from app.modules.user.routes.get_by_id.get_by_id_usecase import GetByIdUsecase
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock


class TestGetByIdUsecase:
    @pytest.fixture
    def user_repository(self):
        """Get the user repository mock"""
        return UserRepositoryMock()

    @pytest.fixture
    def use_case(self, user_repository):
        """Create a GetByIdUsecase instance with the repository"""
        return GetByIdUsecase(repo=user_repository)

    # ==================== VALID SCENARIOS ====================
    
    def test_use_case_initialization(self, user_repository):
        """Test that GetByIdUsecase initializes correctly with repo"""
        use_case = GetByIdUsecase(repo=user_repository)
        assert use_case.repo is user_repository
        assert hasattr(use_case, "repo")

    def test_use_case_initialization_with_positional_argument(self, user_repository):
        """Test that initialization works with positional argument"""
        use_case = GetByIdUsecase(user_repository)
        assert use_case.repo is user_repository

    def test_call_is_callable(self, use_case):
        """Test that use_case instance is callable via __call__ method"""
        assert callable(use_case)

    def test_call_with_admin_user_id_returns_admin_user(self, use_case):
        """Test that calling use_case with admin user ID returns admin user"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        result = use_case(admin_user_id)
        
        assert isinstance(result, User)
        assert result.email == "admin@example.com"
        assert result.role == ROLE.ADMIN
        assert result.is_active is True

    def test_call_with_user1_id_returns_user1(self, use_case):
        """Test that calling use_case with user1 ID returns user1"""
        user1_id = "93bc6ada-c0d1-7054-26ab-e17454c48ae6"
        result = use_case(user1_id)
        
        assert isinstance(result, User)
        assert result.email == "user1@example.com"
        assert result.role == ROLE.USER
        assert result.is_active is True

    def test_call_with_user2_id_returns_user2(self, use_case):
        """Test that calling use_case with user2 ID returns user2"""
        user2_id = "93bc6ada-c0e1-7054-26ab-e17414c48ae9"
        result = use_case(user2_id)
        
        assert isinstance(result, User)
        assert result.email == "user2@example.com"
        assert result.role == ROLE.USER
        assert result.is_active is False

    def test_returned_user_is_user_entity(self, use_case):
        """Test that returned object is a User entity"""
        result = use_case("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        assert isinstance(result, User)

    def test_returned_user_has_required_attributes(self, use_case):
        """Test that returned user has all required attributes"""
        result = use_case("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert hasattr(result, "id")
        assert hasattr(result, "email")
        assert hasattr(result, "hashed_password")
        assert hasattr(result, "role")
        assert hasattr(result, "is_active")
        assert hasattr(result, "created_at_ms")

    def test_returned_user_has_valid_id(self, use_case):
        """Test that returned user has a valid id"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        result = use_case(admin_user_id)
        
        assert result.id is not None
        assert isinstance(result.id, str)
        assert len(result.id) > 0

    def test_returned_user_has_valid_email(self, use_case):
        """Test that returned user has a valid email"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        result = use_case(admin_user_id)
        
        assert result.email is not None
        assert isinstance(result.email, str)
        assert "@" in result.email

    def test_returned_admin_user_has_valid_role(self, use_case):
        """Test that admin user has valid role"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        result = use_case(admin_user_id)
        
        assert result.role.value == "ADMIN"

    def test_returned_regular_user_has_valid_role(self, use_case):
        """Test that regular user has valid role"""
        user1_id = "93bc6ada-c0d1-7054-26ab-e17454c48ae6"
        result = use_case(user1_id)
        
        assert result.role == ROLE.USER

    def test_different_user_ids_return_different_users(self, use_case):
        """Test that different user IDs return different users"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        user1_id = "93bc6ada-c0d1-7054-26ab-e17454c48ae6"
        user2_id = "93bc6ada-c0e1-7054-26ab-e17414c48ae9"
        
        user1 = use_case(admin_user_id)
        user2 = use_case(user1_id)
        user3 = use_case(user2_id)
        
        assert user1.email != user2.email
        assert user2.email != user3.email
        assert user1.email != user3.email

    def test_same_user_id_returns_same_user(self, use_case):
        """Test that same user ID returns the same user"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        user1_call1 = use_case(admin_user_id)
        user1_call2 = use_case(admin_user_id)
        
        assert user1_call1.email == user1_call2.email
        assert user1_call1.id == user1_call2.id
        assert user1_call1.role == user1_call2.role

    def test_returned_user_has_created_at_ms(self, use_case):
        """Test that returned user has created_at_ms attribute"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        result = use_case(admin_user_id)
        
        assert result.created_at_ms is not None
        assert isinstance(result.created_at_ms, (int, float))
        assert result.created_at_ms > 0
