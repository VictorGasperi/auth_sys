import pytest
from app.modules.user.routes.get_all.get_all_controller import GetAllController
from app.modules.user.routes.get_all.get_all_usecase import GetAllUseCase
from app.modules.user.routes.get_all.get_all_viewmodel import GetAllViewModel
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.environments import Environments
from fastapi import HTTPException


class TestGetAllController:
    @pytest.fixture
    def user_repository(self):
        """Get the user repository from Environments"""
        return Environments.get_user_repo()()

    @pytest.fixture
    def use_case(self, user_repository):
        """Create a GetAllUseCase instance with the repository"""
        return GetAllUseCase(user_repository=user_repository)

    @pytest.fixture
    def controller(self, use_case):
        """Create a GetAllController instance with the use case"""
        return GetAllController(usecase=use_case)

    # ==================== VALID SCENARIOS ====================
    
    def test_controller_initialization(self, use_case):
        """Test that GetAllController initializes correctly with usecase"""
        controller = GetAllController(usecase=use_case)
        assert controller.usecase is use_case
        assert hasattr(controller, "usecase")

    def test_controller_initialization_with_positional_argument(self, use_case):
        """Test that initialization works with positional argument"""
        controller = GetAllController(use_case)
        assert controller.usecase is use_case

    def test_controller_has_usecase_attribute(self, controller, use_case):
        """Test that controller has usecase attribute"""
        assert hasattr(controller, "usecase")
        assert controller.usecase == use_case

    def test_controller_is_callable(self, controller):
        """Test that controller instance is callable via __call__ method"""
        assert callable(controller)

    def test_call_returns_dict(self, controller):
        """Test that calling controller returns a dictionary"""
        result = controller(None)
        assert isinstance(result, dict)

    def test_call_contains_users_key(self, controller):
        """Test that controller response contains 'users' key"""
        result = controller(None)
        assert "users" in result

    def test_call_contains_message_key(self, controller):
        """Test that controller response contains 'message' key"""
        result = controller(None)
        assert "message" in result
        assert result["message"] == "The users were retrieved"

    def test_call_users_is_list(self, controller):
        """Test that controller response 'users' value is a list"""
        result = controller(None)
        assert isinstance(result["users"], list)

    def test_call_returns_three_users(self, controller):
        """Test that controller returns 3 users from mock repository"""
        result = controller(None)
        assert len(result["users"]) == 3

    def test_call_users_are_dicts(self, controller):
        """Test that all users in response are dictionaries"""
        result = controller(None)
        assert all(isinstance(user, dict) for user in result["users"])

    def test_call_users_have_required_fields(self, controller):
        """Test that all users have required fields"""
        result = controller(None)
        
        for user in result["users"]:
            assert "id" in user
            assert "email" in user
            assert "role" in user
            assert "is_active" in user
            assert "created_at_ms" in user

    def test_call_users_do_not_have_hashed_password(self, controller):
        """Test that users do not expose hashed_password"""
        result = controller(None)
        
        for user in result["users"]:
            assert "hashed_password" not in user

    def test_call_contains_admin_user(self, controller):
        """Test that response contains admin user"""
        result = controller(None)
        emails = [user["email"] for user in result["users"]]
        assert "admin@example.com" in emails

    def test_call_contains_regular_users(self, controller):
        """Test that response contains regular users"""
        result = controller(None)
        emails = [user["email"] for user in result["users"]]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    def test_call_admin_has_correct_role(self, controller):
        """Test that admin user has ADMIN role"""
        result = controller(None)
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["role"] == ROLE.ADMIN

    def test_call_regular_users_have_user_role(self, controller):
        """Test that regular users have USER role"""
        result = controller(None)
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user1["role"] == ROLE.USER
        assert user2["role"] == ROLE.USER

    def test_call_admin_is_active(self, controller):
        """Test that admin user is active"""
        result = controller(None)
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["is_active"] is True

    def test_call_user2_is_inactive(self, controller):
        """Test that user2 is inactive"""
        result = controller(None)
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user2["is_active"] is False

    def test_call_multiple_times_returns_consistent_results(self, controller):
        """Test that multiple calls return consistent results"""
        result1 = controller(None)
        result2 = controller(None)
        
        assert len(result1["users"]) == len(result2["users"])
        assert result1["message"] == result2["message"]

    def test_integration_repository_to_controller(self, user_repository):
        """Test full integration: repository → use case → controller"""
        # Create use case with repository
        use_case = GetAllUseCase(user_repository=user_repository)
        
        # Create controller with use case
        controller = GetAllController(usecase=use_case)
        
        # Call controller
        result = controller(None)
        
        # Validate result
        assert isinstance(result, dict)
        assert "users" in result
        assert "message" in result
        assert len(result["users"]) == 3

    def test_controller_uses_usecase_correctly(self, user_repository):
        """Test that controller properly uses the usecase"""
        use_case = GetAllUseCase(user_repository=user_repository)
        controller = GetAllController(usecase=use_case)
        
        result = controller(None)
        
        # Should get same data as calling usecase directly
        users_from_usecase = use_case()
        assert len(result["users"]) == len(users_from_usecase)

    def test_controller_creates_viewmodel_correctly(self, controller):
        """Test that controller creates viewmodel correctly"""
        result = controller(None)
        
        # Result should match what GetAllViewModel.to_dict() would return
        assert "users" in result
        assert "message" in result

    # ==================== INVALID DATA ASSERTIONS ====================
    # These tests assert INCORRECT data to validate what comes from the database

    def test_incorrect_user_count_in_response(self, controller):
        """Test that asserting wrong user count fails - validates actual count is 3"""
        result = controller(None)
        
        # Should NOT be these counts
        assert len(result["users"]) != 0
        assert len(result["users"]) != 5
        assert len(result["users"]) != 10

    def test_incorrect_response_keys(self, controller):
        """Test that asserting wrong keys fails - validates correct keys"""
        result = controller(None)
        
        # Should NOT have these keys
        assert "user_list" not in result
        assert "data" not in result
        assert "items" not in result
        assert "error" not in result

    def test_incorrect_emails_in_response(self, controller):
        """Test that asserting wrong emails fails - validates actual emails"""
        result = controller(None)
        emails = [user["email"] for user in result["users"]]
        
        # These emails should NOT be in the result
        assert "wrong@example.com" not in emails
        assert "fake@example.com" not in emails
        assert "test@test.com" not in emails

    def test_incorrect_hashed_password_presence(self, controller):
        """Test that hashed_password is NOT in response"""
        result = controller(None)
        
        for user in result["users"]:
            assert "hashed_password" not in user
            assert "password" not in user

    def test_incorrect_response_type(self, controller):
        """Test that asserting wrong response type fails - validates dict"""
        result = controller(None)
        
        # Should NOT be these types
        assert not isinstance(result, list)
        assert not isinstance(result, str)
        assert result is not None

    def test_incorrect_users_value_type(self, controller):
        """Test that asserting wrong users value type fails - validates list"""
        result = controller(None)
        
        # 'users' value should NOT be these types
        assert not isinstance(result["users"], dict)
        assert not isinstance(result["users"], str)

    def test_incorrect_admin_count(self, controller):
        """Test that asserting wrong admin count fails - validates 1 admin"""
        result = controller(None)
        admin_users = [user for user in result["users"] if user["role"] == ROLE.ADMIN]
        
        # Should NOT be these counts
        assert len(admin_users) != 0
        assert len(admin_users) != 2
        assert len(admin_users) != 3

    def test_incorrect_regular_user_count(self, controller):
        """Test that asserting wrong regular user count fails - validates 2 users"""
        result = controller(None)
        regular_users = [user for user in result["users"] if user["role"] == ROLE.USER]
        
        # Should NOT be these counts
        assert len(regular_users) != 0
        assert len(regular_users) != 1
        assert len(regular_users) != 3

    def test_incorrect_message_value(self, controller):
        """Test that asserting wrong message fails - validates correct message"""
        result = controller(None)
        
        # Message should NOT be these values
        assert result["message"] != "Error"
        assert result["message"] != "Failed"
        assert result["message"] != ""

    def test_incorrect_empty_response(self, controller):
        """Test that asserting empty response fails - validates users exist"""
        result = controller(None)
        
        # Response should NOT be empty
        assert result != {}
        assert len(result["users"]) > 0