import pytest
from app.modules.user.routes.get_all import get_all_presenter
from app.modules.user.routes.get_all.get_all_controller import GetAllController
from app.modules.user.routes.get_all.get_all_usecase import GetAllUseCase
from app.shared.domain.enums.role import ROLE
from app.shared.environments import Environments


class TestGetAllPresenter:

    # ==================== VALID SCENARIOS ====================
    
    def test_presenter_has_repo_instance(self):
        """Test that presenter module has repository instance"""
        assert hasattr(get_all_presenter, "repo")
        assert get_all_presenter.repo is not None

    def test_presenter_has_usecase_instance(self):
        """Test that presenter module has usecase instance"""
        assert hasattr(get_all_presenter, "usecase")
        assert get_all_presenter.usecase is not None

    def test_presenter_has_controller_instance(self):
        """Test that presenter module has controller instance"""
        assert hasattr(get_all_presenter, "controller")
        assert get_all_presenter.controller is not None

    def test_presenter_has_handler_function(self):
        """Test that presenter module has handler function"""
        assert hasattr(get_all_presenter, "handler")
        assert callable(get_all_presenter.get_all_handler)

    def test_presenter_usecase_is_get_all_usecase_instance(self):
        """Test that usecase is instance of GetAllUseCase"""
        assert isinstance(get_all_presenter.usecase, GetAllUseCase)

    def test_presenter_controller_is_get_all_controller_instance(self):
        """Test that controller is instance of GetAllController"""
        assert isinstance(get_all_presenter.controller, GetAllController)

    def test_presenter_controller_has_usecase(self):
        """Test that controller has the usecase"""
        assert get_all_presenter.controller.usecase is get_all_presenter.usecase

    def test_handler_returns_dict(self):
        """Test that handler returns a dictionary"""
        result = get_all_presenter.get_all_handler(None)
        assert isinstance(result, dict)

    def test_handler_contains_users_key(self):
        """Test that handler response contains 'users' key"""
        result = get_all_presenter.get_all_handler(None)
        assert "users" in result

    def test_handler_contains_message_key(self):
        """Test that handler response contains 'message' key"""
        result = get_all_presenter.get_all_handler(None)
        assert "message" in result
        assert result["message"] == "The users were retrieved"

    def test_handler_returns_three_users(self):
        """Test that handler returns 3 users from mock repository"""
        result = get_all_presenter.get_all_handler(None)
        assert len(result["users"]) == 3

    def test_handler_users_are_dicts(self):
        """Test that all users in handler response are dictionaries"""
        result = get_all_presenter.get_all_handler(None)
        assert all(isinstance(user, dict) for user in result["users"])

    def test_handler_users_have_required_fields(self):
        """Test that all users have required fields"""
        result = get_all_presenter.get_all_handler(None)
        
        for user in result["users"]:
            assert "id" in user
            assert "email" in user
            assert "role" in user
            assert "is_active" in user
            assert "created_at_ms" in user

    def test_handler_users_do_not_have_hashed_password(self):
        """Test that users do not expose hashed_password"""
        result = get_all_presenter.get_all_handler(None)
        
        for user in result["users"]:
            assert "hashed_password" not in user

    def test_handler_contains_admin_user(self):
        """Test that handler response contains admin user"""
        result = get_all_presenter.get_all_handler(None)
        emails = [user["email"] for user in result["users"]]
        assert "admin@example.com" in emails

    def test_handler_contains_regular_users(self):
        """Test that handler response contains regular users"""
        result = get_all_presenter.get_all_handler(None)
        emails = [user["email"] for user in result["users"]]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    def test_handler_admin_has_correct_role(self):
        """Test that admin user has ADMIN role"""
        result = get_all_presenter.get_all_handler(None)
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["role"] == ROLE.ADMIN

    def test_handler_regular_users_have_user_role(self):
        """Test that regular users have USER role"""
        result = get_all_presenter.get_all_handler(None)
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user1["role"] == ROLE.USER
        assert user2["role"] == ROLE.USER

    def test_handler_admin_is_active(self):
        """Test that admin user is active"""
        result = get_all_presenter.get_all_handler(None)
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["is_active"] is True

    def test_handler_user2_is_inactive(self):
        """Test that user2 is inactive"""
        result = get_all_presenter.get_all_handler(None)
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user2["is_active"] is False

    def test_handler_multiple_calls_return_consistent_results(self):
        """Test that multiple handler calls return consistent results"""
        result1 = get_all_presenter.get_all_handler(None)
        result2 = get_all_presenter.get_all_handler(None)
        
        assert len(result1["users"]) == len(result2["users"])
        assert result1["message"] == result2["message"]

    def test_presenter_full_integration(self):
        """Test full integration through presenter handler"""
        result = get_all_presenter.get_all_handler(None)
        
        # Validate complete flow
        assert isinstance(result, dict)
        assert "users" in result
        assert "message" in result
        assert len(result["users"]) == 3
        assert all(isinstance(user, dict) for user in result["users"])

    def test_handler_uses_controller_correctly(self):
        """Test that handler properly uses the controller"""
        result = get_all_presenter.get_all_handler(None)
        
        # Should get same result as calling controller directly
        controller_result = get_all_presenter.controller(None)
        assert result == controller_result

    def test_handler_users_have_unique_ids(self):
        """Test that all users have unique IDs"""
        result = get_all_presenter.get_all_handler(None)
        user_ids = [user["id"] for user in result["users"]]
        assert len(user_ids) == len(set(user_ids))

    def test_handler_users_have_unique_emails(self):
        """Test that all users have unique emails"""
        result = get_all_presenter.get_all_handler(None)
        user_emails = [user["email"] for user in result["users"]]
        assert len(user_emails) == len(set(user_emails))

    def test_handler_specific_admin_id(self):
        """Test that admin has correct ID"""
        result = get_all_presenter.get_all_handler(None)
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["id"] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"

    def test_handler_specific_user1_id(self):
        """Test that user1 has correct ID"""
        result = get_all_presenter.get_all_handler(None)
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        assert user1["id"] == "93bc6ada-c0d1-7054-26ab-e17454c48ae6"

    def test_handler_specific_user2_id(self):
        """Test that user2 has correct ID"""
        result = get_all_presenter.get_all_handler(None)
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user2["id"] == "93bc6ada-c0e1-7054-26ab-e17414c48ae9"

    def test_handler_preserves_user_order(self):
        """Test that handler preserves user order"""
        result = get_all_presenter.get_all_handler(None)
        assert result["users"][0]["email"] == "admin@example.com"
        assert result["users"][1]["email"] == "user1@example.com"
        assert result["users"][2]["email"] == "user2@example.com"

    # ==================== INVALID DATA ASSERTIONS ====================
    # These tests assert INCORRECT data to validate what comes from the database

    def test_incorrect_user_count_in_handler_response(self):
        """Test that asserting wrong user count fails - validates actual count is 3"""
        result = get_all_presenter.get_all_handler(None)
        
        # Should NOT be these counts
        assert len(result["users"]) != 0
        assert len(result["users"]) != 5
        assert len(result["users"]) != 10

    def test_incorrect_response_keys_in_handler(self):
        """Test that asserting wrong keys fails - validates correct keys"""
        result = get_all_presenter.get_all_handler(None)
        
        # Should NOT have these keys
        assert "user_list" not in result
        assert "data" not in result
        assert "items" not in result
        assert "error" not in result

    def test_incorrect_emails_in_handler_response(self):
        """Test that asserting wrong emails fails - validates actual emails"""
        result = get_all_presenter.get_all_handler(None)
        emails = [user["email"] for user in result["users"]]
        
        # These emails should NOT be in the result
        assert "wrong@example.com" not in emails
        assert "fake@example.com" not in emails
        assert "test@test.com" not in emails

    def test_incorrect_hashed_password_in_handler_response(self):
        """Test that hashed_password is NOT exposed in handler response"""
        result = get_all_presenter.get_all_handler(None)
        
        for user in result["users"]:
            assert "hashed_password" not in user
            assert "password" not in user

    def test_incorrect_response_type_from_handler(self):
        """Test that asserting wrong response type fails - validates dict"""
        result = get_all_presenter.get_all_handler(None)
        
        # Should NOT be these types
        assert not isinstance(result, list)
        assert not isinstance(result, str)
        assert result is not None

    def test_incorrect_users_value_type_in_handler(self):
        """Test that asserting wrong users value type fails - validates list"""
        result = get_all_presenter.get_all_handler(None)
        
        # 'users' value should NOT be these types
        assert not isinstance(result["users"], dict)
        assert not isinstance(result["users"], str)

    def test_incorrect_admin_count_in_handler(self):
        """Test that asserting wrong admin count fails - validates 1 admin"""
        result = get_all_presenter.get_all_handler(None)
        admin_users = [user for user in result["users"] if user["role"] == ROLE.ADMIN]
        
        # Should NOT be these counts
        assert len(admin_users) != 0
        assert len(admin_users) != 2
        assert len(admin_users) != 3

    def test_incorrect_regular_user_count_in_handler(self):
        """Test that asserting wrong regular user count fails - validates 2 users"""
        result = get_all_presenter.get_all_handler(None)
        regular_users = [user for user in result["users"] if user["role"] == ROLE.USER]
        
        # Should NOT be these counts
        assert len(regular_users) != 0
        assert len(regular_users) != 1
        assert len(regular_users) != 3

    def test_incorrect_message_value_in_handler(self):
        """Test that asserting wrong message fails - validates correct message"""
        result = get_all_presenter.get_all_handler(None)
        
        # Message should NOT be these values
        assert result["message"] != "Error"
        assert result["message"] != "Failed"
        assert result["message"] != ""

    def test_incorrect_empty_response_from_handler(self):
        """Test that asserting empty response fails - validates users exist"""
        result = get_all_presenter.get_all_handler(None)
        
        # Response should NOT be empty
        assert result != {}
        assert len(result["users"]) > 0

    def test_incorrect_admin_email_in_handler(self):
        """Test that asserting wrong admin email fails - validates admin@example.com"""
        result = get_all_presenter.get_all_handler(None)
        admin_users = [user for user in result["users"] if user["role"] == ROLE.ADMIN]
        
        # Admin email should NOT be these values
        assert admin_users[0]["email"] != "wrongadmin@example.com"
        assert admin_users[0]["email"] != "user1@example.com"
        assert admin_users[0]["email"] != "user2@example.com"

    def test_incorrect_admin_status_in_handler(self):
        """Test that asserting admin is inactive fails - validates admin is active"""
        result = get_all_presenter.get_all_handler(None)
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        
        # Admin should NOT be inactive
        assert admin["is_active"] is not False

    def test_incorrect_user2_status_in_handler(self):
        """Test that asserting user2 is active fails - validates user2 is inactive"""
        result = get_all_presenter.get_all_handler(None)
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        
        # user2 should NOT be active
        assert user2["is_active"] is not True

    def test_incorrect_user1_status_in_handler(self):
        """Test that asserting user1 is inactive fails - validates user1 is active"""
        result = get_all_presenter.get_all_handler(None)
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        
        # user1 should NOT be inactive
        assert user1["is_active"] is not False

    def test_incorrect_email_domains_in_handler(self):
        """Test that asserting wrong email domains fails - validates example.com"""
        result = get_all_presenter.get_all_handler(None)
        
        for user in result["users"]:
            # Should NOT have these domains
            assert "gmail.com" not in user["email"]
            assert "yahoo.com" not in user["email"]
            assert "hotmail.com" not in user["email"]
            assert "test.com" not in user["email"]

    def test_all_users_not_having_same_role_in_handler(self):
        """Test that not all users have same role - validates role diversity"""
        result = get_all_presenter.get_all_handler(None)
        roles = [user["role"] for user in result["users"]]
        
        # Should NOT all be the same role
        assert not all(role == ROLE.ADMIN for role in roles)
        assert not all(role == ROLE.USER for role in roles)

    def test_all_users_not_having_same_status_in_handler(self):
        """Test that not all users have same status - validates status diversity"""
        result = get_all_presenter.get_all_handler(None)
        statuses = [user["is_active"] for user in result["users"]]
        
        # Should NOT all be active or all be inactive
        assert not all(status is True for status in statuses)
        assert not all(status is False for status in statuses)
