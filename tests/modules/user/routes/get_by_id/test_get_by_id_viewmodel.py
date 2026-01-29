import pytest
from app.modules.user.routes.get_by_id.get_by_id_viewmodel import GetByIdViewmodel
from app.modules.user.routes.get_by_id.get_by_id_usecase import GetByIdUsecase
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock


class TestGetByIdViewmodel:
    @pytest.fixture
    def user_repository(self):
        """Get the user repository mock"""
        return UserRepositoryMock()

    @pytest.fixture
    def use_case(self, user_repository):
        """Create a GetByIdUsecase instance with the repository"""
        return GetByIdUsecase(repo=user_repository)

    @pytest.fixture
    def user_from_usecase(self, use_case):
        """Get admin user by calling the use case"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        return use_case(admin_user_id)

    @pytest.fixture
    def viewmodel(self, user_from_usecase):
        """Create a GetByIdViewmodel instance with a user from use case"""
        return GetByIdViewmodel(user=user_from_usecase)

    # ==================== VALID SCENARIOS ====================
    
    def test_viewmodel_initialization(self, user_from_usecase):
        """Test that GetByIdViewmodel initializes correctly with user"""
        viewmodel = GetByIdViewmodel(user=user_from_usecase)
        assert viewmodel.user is user_from_usecase
        assert hasattr(viewmodel, "user")

    def test_viewmodel_initialization_with_positional_argument(self, user_from_usecase):
        """Test that initialization works with positional argument"""
        viewmodel = GetByIdViewmodel(user_from_usecase)
        assert viewmodel.user is user_from_usecase

    def test_viewmodel_has_user_attribute(self, viewmodel, user_from_usecase):
        """Test that viewmodel has user attribute"""
        assert hasattr(viewmodel, "user")
        assert viewmodel.user == user_from_usecase

    def test_viewmodel_has_to_dict_method(self, viewmodel):
        """Test that viewmodel has to_dict method"""
        assert hasattr(viewmodel, "to_dict")
        assert callable(viewmodel.to_dict)

    def test_to_dict_returns_dict(self, viewmodel):
        """Test that to_dict returns a dictionary"""
        result = viewmodel.to_dict()
        assert isinstance(result, dict)

    def test_to_dict_contains_user_key(self, viewmodel):
        """Test that to_dict result contains 'user' key"""
        result = viewmodel.to_dict()
        assert "user" in result

    def test_to_dict_contains_message_key(self, viewmodel):
        """Test that to_dict result contains 'message' key"""
        result = viewmodel.to_dict()
        assert "message" in result
        assert result["message"] == "The user was retrieved"

    def test_to_dict_user_is_dict(self, viewmodel):
        """Test that to_dict 'user' value is a dictionary"""
        result = viewmodel.to_dict()
        assert isinstance(result["user"], dict)

    def test_to_dict_user_has_id_field(self, viewmodel):
        """Test that user in to_dict has 'id' field"""
        result = viewmodel.to_dict()
        user = result["user"]
        assert "id" in user

    def test_to_dict_user_has_email_field(self, viewmodel):
        """Test that user in to_dict has 'email' field"""
        result = viewmodel.to_dict()
        user = result["user"]
        assert "email" in user

    def test_to_dict_user_has_role_field(self, viewmodel):
        """Test that user in to_dict has 'role' field"""
        result = viewmodel.to_dict()
        user = result["user"]
        assert "role" in user

    def test_to_dict_user_has_is_active_field(self, viewmodel):
        """Test that user in to_dict has 'is_active' field"""
        result = viewmodel.to_dict()
        user = result["user"]
        assert "is_active" in user

    def test_to_dict_user_has_created_at_ms_field(self, viewmodel):
        """Test that user in to_dict has 'created_at_ms' field"""
        result = viewmodel.to_dict()
        user = result["user"]
        assert "created_at_ms" in user

    def test_to_dict_user_does_not_have_hashed_password(self, viewmodel):
        """Test that user does not expose hashed_password in to_dict"""
        result = viewmodel.to_dict()
        user = result["user"]
        assert "hashed_password" not in user

    def test_to_dict_returns_correct_user_email(self, viewmodel):
        """Test that to_dict returns the correct admin user email"""
        result = viewmodel.to_dict()
        user = result["user"]
        
        assert user["email"] == "admin@example.com"
        assert user["id"] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"

    def test_to_dict_returns_correct_user_role(self, viewmodel):
        """Test that to_dict returns the correct user role for admin"""
        result = viewmodel.to_dict()
        user = result["user"]
        
        assert user["role"] == ROLE.ADMIN.value

    def test_to_dict_returns_correct_user_active_status(self, viewmodel):
        """Test that to_dict returns the correct user active status"""
        result = viewmodel.to_dict()
        user = result["user"]
        
        assert user["is_active"] is True

    def test_viewmodel_with_different_user(self, use_case):
        """Test viewmodel with user1"""
        user1_id = "93bc6ada-c0d1-7054-26ab-e17454c48ae6"
        user = use_case(user1_id)
        viewmodel = GetByIdViewmodel(user)
        result = viewmodel.to_dict()
        
        assert result["user"]["email"] == "user1@example.com"
        assert result["user"]["role"] == ROLE.USER.value
        assert result["user"]["is_active"] is True

    def test_viewmodel_with_inactive_user(self, use_case):
        """Test viewmodel with inactive user (user2)"""
        user2_id = "93bc6ada-c0e1-7054-26ab-e17414c48ae9"
        user = use_case(user2_id)
        viewmodel = GetByIdViewmodel(user)
        result = viewmodel.to_dict()
        
        assert result["user"]["email"] == "user2@example.com"
        assert result["user"]["role"] == ROLE.USER.value
        assert result["user"]["is_active"] is False

    def test_to_dict_result_structure(self, viewmodel):
        """Test that to_dict result has the expected structure"""
        result = viewmodel.to_dict()
        
        # Should have exactly 2 keys: user and message
        assert len(result) == 2
        assert set(result.keys()) == {"user", "message"}
        
        # Message should be a string
        assert isinstance(result["message"], str)
        assert result["message"] == "The user was retrieved"
        
        # User should be a dictionary with expected fields
        user = result["user"]
        expected_fields = {"id", "email", "role", "is_active", "created_at_ms"}
        assert all(field in user for field in expected_fields)
        
        # Verify no hashed_password is exposed
        assert "hashed_password" not in user
