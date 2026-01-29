import pytest
from fastapi import HTTPException
from app.modules.user.routes.get_by_id.get_by_id_controller import GetByIdController
from app.modules.user.routes.get_by_id.get_by_id_usecase import GetByIdUsecase
from app.shared.domain.enums.role import ROLE
from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock


class QueryParams:
    """Helper class to simulate FastAPI query parameters"""
    def __init__(self, user_id=None):
        self.user_id = user_id
    
    def get(self, key, default=None):
        if key == "user_id":
            return self.user_id
        return default


class RequestObject:
    """Helper class to simulate FastAPI Request object"""
    def __init__(self, user_id=None):
        self.query_params = QueryParams(user_id)


class TestGetByIdController:
    @pytest.fixture
    def user_repository(self):
        """Get the user repository mock"""
        return UserRepositoryMock()

    @pytest.fixture
    def use_case(self, user_repository):
        """Create a GetByIdUsecase instance with the repository"""
        return GetByIdUsecase(repo=user_repository)

    @pytest.fixture
    def controller(self, use_case):
        """Create a GetByIdController instance with the use case"""
        return GetByIdController(usecase=use_case)

    @pytest.fixture
    def admin_user_id(self):
        """Return admin user ID from mock"""
        return "93bc6ada-c0d1-7054-26ab-e17414c48ae3"

    @pytest.fixture
    def user1_id(self):
        """Return user1 ID from mock"""
        return "93bc6ada-c0d1-7054-26ab-e17454c48ae6"

    @pytest.fixture
    def user2_id(self):
        """Return user2 ID from mock"""
        return "93bc6ada-c0e1-7054-26ab-e17414c48ae9"

    # ==================== VALID SCENARIOS ====================
    
    def test_controller_initialization(self, use_case):
        """Test that GetByIdController initializes correctly with usecase"""
        controller = GetByIdController(usecase=use_case)
        assert controller.usecase is use_case
        assert hasattr(controller, "usecase")

    def test_controller_initialization_with_positional_argument(self, use_case):
        """Test that initialization works with positional argument"""
        controller = GetByIdController(use_case)
        assert controller.usecase is use_case

    def test_controller_has_usecase_attribute(self, controller, use_case):
        """Test that controller has usecase attribute"""
        assert hasattr(controller, "usecase")
        assert controller.usecase == use_case

    def test_controller_is_callable(self, controller):
        """Test that controller instance is callable via __call__ method"""
        assert callable(controller)

    def test_call_with_valid_user_id_returns_dict(self, controller, admin_user_id):
        """Test that calling controller with valid user_id returns a dictionary"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        assert isinstance(result, dict)

    def test_call_with_valid_user_id_contains_user_key(self, controller, admin_user_id):
        """Test that controller response contains 'user' key"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        assert "user" in result

    def test_call_with_valid_user_id_contains_message_key(self, controller, admin_user_id):
        """Test that controller response contains 'message' key"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        assert "message" in result
        assert result["message"] == "The user was retrieved"

    def test_call_with_valid_user_id_user_is_dict(self, controller, admin_user_id):
        """Test that controller response 'user' value is a dictionary"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        assert isinstance(result["user"], dict)

    def test_call_with_valid_user_id_user_has_required_fields(self, controller, admin_user_id):
        """Test that returned user has required fields"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        user = result["user"]
        
        assert "id" in user
        assert "email" in user
        assert "role" in user
        assert "is_active" in user
        assert "created_at_ms" in user

    def test_call_with_valid_user_id_user_does_not_have_hashed_password(self, controller, admin_user_id):
        """Test that user does not expose hashed_password"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        user = result["user"]
        
        assert "hashed_password" not in user

    # ==================== ERROR SCENARIOS ====================
    
    def test_call_without_user_id_raises_http_exception(self, controller):
        """Test that calling controller without user_id raises HTTPException"""
        request = RequestObject(None)
        
        with pytest.raises(HTTPException) as exc_info:
            controller(request)
        
        assert exc_info.value.status_code == 400
        assert "user_id must be provided" in exc_info.value.detail

    def test_call_with_empty_string_user_id_raises_http_exception(self, controller):
        """Test that calling controller with empty string user_id raises HTTPException"""
        request = RequestObject("")
        
        with pytest.raises(HTTPException) as exc_info:
            controller(request)
        
        assert exc_info.value.status_code == 400

    def test_call_with_valid_user_id_returns_admin_user(self, controller, admin_user_id):
        """Test that controller returns admin user when requesting admin user ID"""
        request = RequestObject(admin_user_id)
        result = controller(request)
        user = result["user"]
        
        assert user["email"] == "admin@example.com"
        assert user["role"] == ROLE.ADMIN.value

    def test_call_with_user1_id_returns_user1(self, controller, user1_id):
        """Test that controller returns user1 when requesting user1 ID"""
        request = RequestObject(user1_id)
        result = controller(request)
        user = result["user"]
        
        assert user["email"] == "user1@example.com"
        assert user["role"] == ROLE.USER.value

    def test_call_with_user2_id_returns_user2(self, controller, user2_id):
        """Test that controller returns user2 when requesting user2 ID"""
        request = RequestObject(user2_id)
        result = controller(request)
        user = result["user"]
        
        assert user["email"] == "user2@example.com"
        assert user["role"] == ROLE.USER.value
        assert user["is_active"] is False
