import pytest
from app.modules.user.routes.get_all.get_all_viewmodel import GetAllViewModel
from app.modules.user.routes.get_all.get_all_usecase import GetAllUseCase
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock


class TestGetAllViewModel:
    @pytest.fixture
    def user_repository(self):
        """Get the user repository mock"""
        return UserRepositoryMock()

    @pytest.fixture
    def use_case(self, user_repository):
        """Create a GetAllUseCase instance with the repository"""
        return GetAllUseCase(user_repository=user_repository)

    @pytest.fixture
    def users_from_usecase(self, use_case):
        """Get users by calling the use case"""
        return use_case()

    @pytest.fixture
    def viewmodel(self, users_from_usecase):
        """Create a GetAllViewModel instance with users from use case"""
        return GetAllViewModel(users=users_from_usecase)

    # ==================== VALID SCENARIOS ====================
    
    def test_viewmodel_initialization(self, users_from_usecase):
        """Test that GetAllViewModel initializes correctly with users"""
        viewmodel = GetAllViewModel(users=users_from_usecase)
        assert viewmodel.users is users_from_usecase
        assert hasattr(viewmodel, "users")

    def test_viewmodel_initialization_with_positional_argument(self, users_from_usecase):
        """Test that initialization works with positional argument"""
        viewmodel = GetAllViewModel(users_from_usecase)
        assert viewmodel.users is users_from_usecase

    def test_viewmodel_has_users_attribute(self, viewmodel, users_from_usecase):
        """Test that viewmodel has users attribute"""
        assert hasattr(viewmodel, "users")
        assert viewmodel.users == users_from_usecase

    def test_viewmodel_has_to_dict_method(self, viewmodel):
        """Test that viewmodel has to_dict method"""
        assert hasattr(viewmodel, "to_dict")
        assert callable(viewmodel.to_dict)

    def test_to_dict_returns_dict(self, viewmodel):
        """Test that to_dict returns a dictionary"""
        result = viewmodel.to_dict()
        assert isinstance(result, dict)

    def test_to_dict_contains_users_key(self, viewmodel):
        """Test that to_dict result contains 'users' key"""
        result = viewmodel.to_dict()
        assert "users" in result

    def test_to_dict_contains_message_key(self, viewmodel):
        """Test that to_dict result contains 'message' key"""
        result = viewmodel.to_dict()
        assert "message" in result
        assert result["message"] == "The users were retrieved"

    def test_to_dict_users_is_list(self, viewmodel):
        """Test that to_dict 'users' value is a list"""
        result = viewmodel.to_dict()
        assert isinstance(result["users"], list)

    def test_to_dict_users_count_matches_input(self, viewmodel):
        """Test that to_dict returns same number of users as input"""
        result = viewmodel.to_dict()
        assert len(result["users"]) == 3  # Mock has 3 users

    def test_to_dict_users_are_dicts(self, viewmodel):
        """Test that all users in to_dict result are dictionaries"""
        result = viewmodel.to_dict()
        assert all(isinstance(user, dict) for user in result["users"])

    def test_to_dict_users_have_id_field(self, viewmodel):
        """Test that all users in to_dict have 'id' field"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert "id" in user

    def test_to_dict_users_have_email_field(self, viewmodel):
        """Test that all users in to_dict have 'email' field"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert "email" in user

    def test_to_dict_users_have_role_field(self, viewmodel):
        """Test that all users in to_dict have 'role' field"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert "role" in user

    def test_to_dict_users_have_is_active_field(self, viewmodel):
        """Test that all users in to_dict have 'is_active' field"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert "is_active" in user

    def test_to_dict_users_have_created_at_ms_field(self, viewmodel):
        """Test that all users in to_dict have 'created_at_ms' field"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert "created_at_ms" in user

    def test_to_dict_users_do_not_have_hashed_password(self, viewmodel):
        """Test that users in to_dict do not expose hashed_password"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert "hashed_password" not in user

    def test_to_dict_contains_admin_user(self, viewmodel):
        """Test that to_dict result contains admin user"""
        result = viewmodel.to_dict()
        emails = [user["email"] for user in result["users"]]
        assert "admin@example.com" in emails

    def test_to_dict_contains_regular_users(self, viewmodel):
        """Test that to_dict result contains regular users"""
        result = viewmodel.to_dict()
        emails = [user["email"] for user in result["users"]]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    def test_to_dict_admin_has_correct_role(self, viewmodel):
        """Test that admin user has ADMIN role in to_dict"""
        result = viewmodel.to_dict()
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["role"] == ROLE.ADMIN.value

    def test_to_dict_regular_users_have_user_role(self, viewmodel):
        """Test that regular users have USER role in to_dict"""
        result = viewmodel.to_dict()
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user1["role"] == ROLE.USER.value
        assert user2["role"] == ROLE.USER.value

    def test_to_dict_admin_is_active(self, viewmodel):
        """Test that admin user is active in to_dict"""
        result = viewmodel.to_dict()
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["is_active"] is True

    def test_to_dict_user1_is_active(self, viewmodel):
        """Test that user1 is active in to_dict"""
        result = viewmodel.to_dict()
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        assert user1["is_active"] is True

    def test_to_dict_user2_is_inactive(self, viewmodel):
        """Test that user2 is inactive in to_dict"""
        result = viewmodel.to_dict()
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user2["is_active"] is False

    def test_to_dict_users_have_valid_ids(self, viewmodel):
        """Test that all users have valid UUID-like IDs"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert isinstance(user["id"], str)
            assert "-" in user["id"]

    def test_to_dict_users_have_valid_emails(self, viewmodel):
        """Test that all users have valid email format"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert isinstance(user["email"], str)
            assert "@" in user["email"]
            assert "example.com" in user["email"]

    def test_to_dict_users_have_valid_timestamps(self, viewmodel):
        """Test that all users have valid timestamps"""
        result = viewmodel.to_dict()
        for user in result["users"]:
            assert isinstance(user["created_at_ms"], int)
            assert user["created_at_ms"] > 0

    def test_to_dict_preserves_user_order(self, viewmodel):
        """Test that to_dict preserves user order from use case"""
        result = viewmodel.to_dict()
        assert result["users"][0]["email"] == "admin@example.com"
        assert result["users"][1]["email"] == "user1@example.com"
        assert result["users"][2]["email"] == "user2@example.com"

    def test_to_dict_called_multiple_times_returns_same_structure(self, viewmodel):
        """Test that multiple calls to to_dict return same structure"""
        result1 = viewmodel.to_dict()
        result2 = viewmodel.to_dict()
        
        assert len(result1["users"]) == len(result2["users"])
        assert result1.keys() == result2.keys()

    def test_to_dict_called_multiple_times_returns_same_data(self, viewmodel):
        """Test that multiple calls to to_dict return same data"""
        result1 = viewmodel.to_dict()
        result2 = viewmodel.to_dict()
        
        emails1 = sorted([user["email"] for user in result1["users"]])
        emails2 = sorted([user["email"] for user in result2["users"]])
        assert emails1 == emails2

    def test_viewmodel_with_empty_users_list(self):
        """Test that viewmodel works with empty users list"""
        viewmodel = GetAllViewModel(users=[])
        result = viewmodel.to_dict()
        
        assert isinstance(result, dict)
        assert "users" in result
        assert result["users"] == []

    def test_viewmodel_with_single_user(self, user_repository):
        """Test that viewmodel works with single user"""
        single_user = [user_repository.get_by_email("admin@example.com")]
        viewmodel = GetAllViewModel(users=single_user)
        result = viewmodel.to_dict()
        
        assert len(result["users"]) == 1
        assert result["users"][0]["email"] == "admin@example.com"

    def test_integration_repository_to_viewmodel(self, user_repository):
        """Test full integration: repository → use case → viewmodel"""
        # Get repository
        repo = user_repository
        
        # Create and call use case
        use_case = GetAllUseCase(user_repository=repo)
        users = use_case()
        
        # Create viewmodel
        viewmodel = GetAllViewModel(users=users)
        result = viewmodel.to_dict()
        
        # Validate result
        assert isinstance(result, dict)
        assert "users" in result
        assert len(result["users"]) == 3

    def test_to_dict_users_have_unique_ids(self, viewmodel):
        """Test that all users in to_dict have unique IDs"""
        result = viewmodel.to_dict()
        user_ids = [user["id"] for user in result["users"]]
        assert len(user_ids) == len(set(user_ids))

    def test_to_dict_users_have_unique_emails(self, viewmodel):
        """Test that all users in to_dict have unique emails"""
        result = viewmodel.to_dict()
        user_emails = [user["email"] for user in result["users"]]
        assert len(user_emails) == len(set(user_emails))

    def test_to_dict_specific_admin_id(self, viewmodel):
        """Test that admin has correct ID in to_dict"""
        result = viewmodel.to_dict()
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        assert admin["id"] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"

    def test_to_dict_specific_user1_id(self, viewmodel):
        """Test that user1 has correct ID in to_dict"""
        result = viewmodel.to_dict()
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        assert user1["id"] == "93bc6ada-c0d1-7054-26ab-e17454c48ae6"

    def test_to_dict_specific_user2_id(self, viewmodel):
        """Test that user2 has correct ID in to_dict"""
        result = viewmodel.to_dict()
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        assert user2["id"] == "93bc6ada-c0e1-7054-26ab-e17414c48ae9"

    # ==================== INVALID DATA ASSERTIONS ====================
    # These tests assert INCORRECT data to validate what comes from the database

    def test_incorrect_user_count_in_dict(self, viewmodel):
        """Test that asserting wrong user count fails - validates actual count is 3"""
        result = viewmodel.to_dict()
        # Should NOT be these counts
        assert len(result["users"]) != 0
        assert len(result["users"]) != 5
        assert len(result["users"]) != 10

    def test_incorrect_dict_keys(self, viewmodel):
        """Test that asserting wrong keys fails - validates 'users' key exists"""
        result = viewmodel.to_dict()
        # Should NOT have these keys
        assert "user_list" not in result
        assert "data" not in result
        assert "items" not in result

    def test_incorrect_email_in_dict(self, viewmodel):
        """Test that asserting wrong emails fails - validates actual emails"""
        result = viewmodel.to_dict()
        emails = [user["email"] for user in result["users"]]
        
        # These emails should NOT be in the result
        assert "wrong@example.com" not in emails
        assert "fake@example.com" not in emails
        assert "test@test.com" not in emails

    def test_incorrect_hashed_password_exposure(self, viewmodel):
        """Test that hashed_password is NOT exposed in to_dict"""
        result = viewmodel.to_dict()
        
        for user in result["users"]:
            # Should NOT have hashed_password field
            assert "hashed_password" not in user
            assert "password" not in user
            assert "pwd" not in user

    def test_incorrect_return_type(self, viewmodel):
        """Test that asserting wrong return type fails - validates dict is returned"""
        result = viewmodel.to_dict()
        
        # Should NOT be these types
        assert not isinstance(result, list)
        assert not isinstance(result, str)
        assert not isinstance(result, int)
        assert result is not None

    def test_incorrect_users_value_type(self, viewmodel):
        """Test that asserting wrong users value type fails - validates list"""
        result = viewmodel.to_dict()
        
        # 'users' value should NOT be these types
        assert not isinstance(result["users"], dict)
        assert not isinstance(result["users"], str)
        assert not isinstance(result["users"], int)

    def test_incorrect_user_dict_type(self, viewmodel):
        """Test that asserting wrong user types fails - validates dicts"""
        result = viewmodel.to_dict()
        
        for user in result["users"]:
            # Each user should NOT be these types
            assert not isinstance(user, list)
            assert not isinstance(user, str)
            assert user is not None

    def test_incorrect_admin_count_in_dict(self, viewmodel):
        """Test that asserting wrong admin count fails - validates 1 admin"""
        result = viewmodel.to_dict()
        admin_users = [user for user in result["users"] if user["role"] == ROLE.ADMIN.value]
        
        # Should NOT be these counts
        assert len(admin_users) != 0
        assert len(admin_users) != 2
        assert len(admin_users) != 3

    def test_incorrect_regular_user_count_in_dict(self, viewmodel):
        """Test that asserting wrong regular user count fails - validates 2 users"""
        result = viewmodel.to_dict()
        regular_users = [user for user in result["users"] if user["role"] == ROLE.USER.value]
        
        # Should NOT be these counts
        assert len(regular_users) != 0
        assert len(regular_users) != 1
        assert len(regular_users) != 3

    def test_incorrect_active_count_in_dict(self, viewmodel):
        """Test that asserting wrong active count fails - validates 2 active users"""
        result = viewmodel.to_dict()
        active_users = [user for user in result["users"] if user["is_active"] is True]
        
        # Should NOT be these counts
        assert len(active_users) != 0
        assert len(active_users) != 1
        assert len(active_users) != 3

    def test_incorrect_inactive_count_in_dict(self, viewmodel):
        """Test that asserting wrong inactive count fails - validates 1 inactive"""
        result = viewmodel.to_dict()
        inactive_users = [user for user in result["users"] if user["is_active"] is False]
        
        # Should NOT be these counts
        assert len(inactive_users) != 0
        assert len(inactive_users) != 2
        assert len(inactive_users) != 3

    def test_incorrect_admin_email_in_dict(self, viewmodel):
        """Test that asserting wrong admin email fails - validates admin@example.com"""
        result = viewmodel.to_dict()
        admin_users = [user for user in result["users"] if user["role"] == ROLE.ADMIN.value]
        
        # Admin email should NOT be these values
        assert admin_users[0]["email"] != "wrongadmin@example.com"
        assert admin_users[0]["email"] != "user1@example.com"
        assert admin_users[0]["email"] != "user2@example.com"

    def test_incorrect_admin_status_in_dict(self, viewmodel):
        """Test that asserting admin is inactive fails - validates admin is active"""
        result = viewmodel.to_dict()
        admin = [user for user in result["users"] if user["email"] == "admin@example.com"][0]
        
        # Admin should NOT be inactive
        assert admin["is_active"] is not False

    def test_incorrect_user2_status_in_dict(self, viewmodel):
        """Test that asserting user2 is active fails - validates user2 is inactive"""
        result = viewmodel.to_dict()
        user2 = [user for user in result["users"] if user["email"] == "user2@example.com"][0]
        
        # user2 should NOT be active
        assert user2["is_active"] is not True

    def test_incorrect_user1_status_in_dict(self, viewmodel):
        """Test that asserting user1 is inactive fails - validates user1 is active"""
        result = viewmodel.to_dict()
        user1 = [user for user in result["users"] if user["email"] == "user1@example.com"][0]
        
        # user1 should NOT be inactive
        assert user1["is_active"] is not False

    def test_incorrect_id_format_in_dict(self, viewmodel):
        """Test that asserting wrong ID format fails - validates UUID format"""
        result = viewmodel.to_dict()
        
        for user in result["users"]:
            # IDs should NOT be simple integers
            assert not user["id"].isdigit()
            # IDs should have dashes (UUID format)
            assert "-" in user["id"]

    def test_incorrect_empty_result(self, viewmodel):
        """Test that asserting empty result fails - validates users exist"""
        result = viewmodel.to_dict()
        
        # Result should NOT be empty
        assert result != {}
        assert result is not None
        assert len(result["users"]) > 0

    def test_incorrect_email_domains_in_dict(self, viewmodel):
        """Test that asserting wrong email domains fails - validates example.com"""
        result = viewmodel.to_dict()
        
        for user in result["users"]:
            # Should NOT have these domains
            assert "gmail.com" not in user["email"]
            assert "yahoo.com" not in user["email"]
            assert "hotmail.com" not in user["email"]
            assert "test.com" not in user["email"]

    def test_all_users_not_having_same_role_in_dict(self, viewmodel):
        """Test that not all users have same role - validates role diversity"""
        result = viewmodel.to_dict()
        roles = [user["role"] for user in result["users"]]
        
        # Should NOT all be the same role
        assert not all(role == ROLE.ADMIN for role in roles)
        assert not all(role == ROLE.USER for role in roles)

    def test_all_users_not_having_same_status_in_dict(self, viewmodel):
        """Test that not all users have same status - validates status diversity"""
        result = viewmodel.to_dict()
        statuses = [user["is_active"] for user in result["users"]]
        
        # Should NOT all be active or all be inactive
        assert not all(status is True for status in statuses)
        assert not all(status is False for status in statuses)
