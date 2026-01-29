import pytest
from app.modules.user.routes.get_by_id import get_by_id_presenter
from app.modules.user.routes.get_by_id.get_by_id_controller import GetByIdController
from app.modules.user.routes.get_by_id.get_by_id_usecase import GetByIdUsecase
from app.shared.domain.enums.role import ROLE


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

class TestGetByIdPresenter:

    @pytest.fixture
    def request_with_admin_user_id(self):
        """Create a request-like object with admin user_id"""
        admin_user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        return RequestObject(admin_user_id)

    @pytest.fixture
    def request_with_user1_id(self):
        """Create a request-like object with user1 ID"""
        user1_id = "93bc6ada-c0d1-7054-26ab-e17454c48ae6"
        return RequestObject(user1_id)

    @pytest.fixture
    def request_with_user2_id(self):
        """Create a request-like object with user2 ID"""
        user2_id = "93bc6ada-c0e1-7054-26ab-e17414c48ae9"
        return RequestObject(user2_id)

    # ==================== VALID SCENARIOS ====================
    
    def test_presenter_has_repo_instance(self):
        """Test that presenter module has repository instance"""
        assert hasattr(get_by_id_presenter, "repo")
        assert get_by_id_presenter.repo is not None

    def test_presenter_has_usecase_instance(self):
        """Test that presenter module has usecase instance"""
        assert hasattr(get_by_id_presenter, "usecase")
        assert get_by_id_presenter.usecase is not None

    def test_presenter_has_controller_instance(self):
        """Test that presenter module has controller instance"""
        assert hasattr(get_by_id_presenter, "controller")
        assert get_by_id_presenter.controller is not None

    def test_presenter_has_handler_function(self):
        """Test that presenter module has handler function"""
        assert hasattr(get_by_id_presenter, "get_by_id_handler")
        assert callable(get_by_id_presenter.get_by_id_handler)

    def test_presenter_usecase_is_get_by_id_usecase_instance(self):
        """Test that usecase is instance of GetByIdUsecase"""
        assert isinstance(get_by_id_presenter.usecase, GetByIdUsecase)

    def test_presenter_controller_is_get_by_id_controller_instance(self):
        """Test that controller is instance of GetByIdController"""
        assert isinstance(get_by_id_presenter.controller, GetByIdController)

    def test_presenter_controller_has_usecase(self):
        """Test that controller has the usecase"""
        assert get_by_id_presenter.controller.usecase is get_by_id_presenter.usecase

    def test_handler_with_valid_user_id_returns_dict(self, request_with_admin_user_id):
        """Test that handler with valid user_id returns a dictionary"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        assert isinstance(result, dict)

    def test_handler_with_valid_user_id_contains_user_key(self, request_with_admin_user_id):
        """Test that handler response contains 'user' key"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        assert "user" in result

    def test_handler_with_valid_user_id_contains_message_key(self, request_with_admin_user_id):
        """Test that handler response contains 'message' key"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        assert "message" in result
        assert result["message"] == "The user was retrieved"

    def test_handler_with_valid_user_id_user_is_dict(self, request_with_admin_user_id):
        """Test that handler response 'user' value is a dictionary"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        assert isinstance(result["user"], dict)

    def test_handler_with_valid_user_id_user_has_required_fields(self, request_with_admin_user_id):
        """Test that handler returned user has required fields"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        user = result["user"]
        
        assert "id" in user
        assert "email" in user
        assert "role" in user
        assert "is_active" in user
        assert "created_at_ms" in user

    def test_handler_with_valid_user_id_user_does_not_have_hashed_password(self, request_with_admin_user_id):
        """Test that handler user does not expose hashed_password"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        user = result["user"]
        
        assert "hashed_password" not in user

    def test_handler_returns_admin_user_when_requesting_admin_id(self, request_with_admin_user_id):
        """Test that handler returns admin user when requesting admin user ID"""
        result = get_by_id_presenter.get_by_id_handler(request_with_admin_user_id)
        user = result["user"]
        
        assert user["email"] == "admin@example.com"
        assert user["role"] == ROLE.ADMIN.value

    def test_handler_returns_user1_when_requesting_user1_id(self, request_with_user1_id):
        """Test that handler returns user1 when requesting user1 ID"""
        result = get_by_id_presenter.get_by_id_handler(request_with_user1_id)
        user = result["user"]
        
        assert user["email"] == "user1@example.com"
        assert user["role"] == ROLE.USER.value
        assert user["is_active"] is True

    def test_handler_returns_user2_when_requesting_user2_id(self, request_with_user2_id):
        """Test that handler returns user2 when requesting user2 ID"""
        result = get_by_id_presenter.get_by_id_handler(request_with_user2_id)
        user = result["user"]
        
        assert user["email"] == "user2@example.com"
        assert user["role"] == ROLE.USER.value
        assert user["is_active"] is False
