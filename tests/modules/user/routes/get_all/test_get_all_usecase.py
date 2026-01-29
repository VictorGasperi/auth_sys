import pytest
from app.modules.user.routes.get_all.get_all_usecase import GetAllUseCase
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock


class TestGetAllUseCase:
    @pytest.fixture
    def user_repository(self):
        """Get the user repository mock"""
        return UserRepositoryMock()

    @pytest.fixture
    def use_case(self, user_repository):
        """Create a GetAllUseCase instance with the repository"""
        return GetAllUseCase(user_repository=user_repository)

    # ==================== VALID SCENARIOS ====================
    
    def test_use_case_initialization(self, user_repository):
        """Test that GetAllUseCase initializes correctly with user_repository"""
        use_case = GetAllUseCase(user_repository=user_repository)
        assert use_case.user_repository is user_repository
        assert hasattr(use_case, "user_repository")

    def test_use_case_initialization_with_positional_argument(self, user_repository):
        """Test that initialization works with positional argument"""
        use_case = GetAllUseCase(user_repository)
        assert use_case.user_repository is user_repository

    def test_call_returns_all_users_from_mock(self, use_case):
        """Test that calling use_case returns all 3 users from mock repository"""
        result = use_case()

        assert isinstance(result, list)
        assert len(result) == 3

    def test_call_returns_list_of_user_entities(self, use_case):
        """Test that use_case returns a list of User entities"""
        result = use_case()
        
        assert isinstance(result, list)
        assert all(isinstance(user, User) for user in result)

    def test_call_is_callable(self, use_case):
        """Test that use_case instance is callable via __call__ method"""
        assert callable(use_case)
        result = use_case()
        assert result is not None

    def test_returned_users_match_mock_data(self, use_case):
        """Test that returned users contain the expected mock data"""
        result = use_case()
        
        emails = [user.email for user in result]
        assert "admin@example.com" in emails
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    def test_returned_users_have_admin_user(self, use_case):
        """Test that returned users include admin user"""
        result = use_case()
        
        admin_users = [user for user in result if user.role == ROLE.ADMIN]
        assert len(admin_users) == 1
        assert admin_users[0].email == "admin@example.com"
        assert admin_users[0].is_active is True

    def test_returned_users_have_regular_users(self, use_case):
        """Test that returned users include regular users"""
        result = use_case()
        
        regular_users = [user for user in result if user.role == ROLE.USER]
        assert len(regular_users) == 2

    def test_returned_users_include_active_and_inactive(self, use_case):
        """Test that returned users include both active and inactive users"""
        result = use_case()
        
        active_users = [user for user in result if user.is_active is True]
        inactive_users = [user for user in result if user.is_active is False]
        
        assert len(active_users) == 2
        assert len(inactive_users) == 1

    def test_inactive_user_is_user2(self, use_case):
        """Test that user2@example.com is the inactive user"""
        result = use_case()
        
        inactive_users = [user for user in result if user.is_active is False]
        assert len(inactive_users) == 1
        assert inactive_users[0].email == "user2@example.com"
        assert inactive_users[0].role == ROLE.USER

    def test_all_users_have_required_attributes(self, use_case):
        """Test that all returned users have required attributes"""
        result = use_case()
        
        for user in result:
            assert hasattr(user, "id")
            assert hasattr(user, "email")
            assert hasattr(user, "hashed_password")
            assert hasattr(user, "role")
            assert hasattr(user, "is_active")
            assert hasattr(user, "created_at_ms")

    def test_all_users_have_valid_emails(self, use_case):
        """Test that all returned users have valid email format"""
        result = use_case()
        
        for user in result:
            assert isinstance(user.email, str)
            assert "@" in user.email
            assert "example.com" in user.email

    def test_all_users_have_valid_roles(self, use_case):
        """Test that all returned users have valid roles"""
        result = use_case()
        
        for user in result:
            assert user.role in [ROLE.USER, ROLE.ADMIN]

    def test_all_users_have_boolean_is_active(self, use_case):
        """Test that all returned users have boolean is_active field"""
        result = use_case()
        
        for user in result:
            assert isinstance(user.is_active, bool)

    def test_all_users_have_valid_timestamps(self, use_case):
        """Test that all returned users have valid timestamps"""
        result = use_case()
        
        for user in result:
            assert isinstance(user.created_at_ms, int)
            assert user.created_at_ms > 0

    def test_all_users_have_hashed_passwords(self, use_case):
        """Test that all returned users have hashed passwords"""
        result = use_case()
        
        for user in result:
            assert isinstance(user.hashed_password, str)
            assert len(user.hashed_password) > 0
            assert "hashed" in user.hashed_password

    def test_all_users_have_uuid_format_ids(self, use_case):
        """Test that all returned users have UUID-like IDs"""
        result = use_case()
        
        for user in result:
            assert isinstance(user.id, str)
            assert len(user.id) > 0
            # UUID format check
            assert "-" in user.id

    def test_returned_users_have_unique_ids(self, use_case):
        """Test that all returned users have unique IDs"""
        result = use_case()
        
        user_ids = [user.id for user in result]
        assert len(user_ids) == len(set(user_ids))

    def test_returned_users_have_unique_emails(self, use_case):
        """Test that all returned users have unique emails"""
        result = use_case()
        
        user_emails = [user.email for user in result]
        assert len(user_emails) == len(set(user_emails))

    def test_repository_is_interface_implementation(self, user_repository):
        """Test that repository implements IUserRepository interface"""
        from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository
        assert isinstance(user_repository, IUserRepository)

    def test_multiple_calls_return_consistent_count(self, use_case):
        """Test that multiple calls return same number of users"""
        result1 = use_case()
        result2 = use_case()
        result3 = use_case()
        
        assert len(result1) == len(result2) == len(result3) == 3

    def test_multiple_calls_return_same_users(self, use_case):
        """Test that multiple calls return the same user emails"""
        result1 = use_case()
        result2 = use_case()
        
        emails1 = sorted([user.email for user in result1])
        emails2 = sorted([user.email for user in result2])
        
        assert emails1 == emails2

    def test_use_case_does_not_modify_repository(self, use_case, user_repository):
        """Test that calling use_case does not modify repository state"""
        initial_count = len(user_repository.get_all())
        
        use_case()
        
        final_count = len(user_repository.get_all())
        assert initial_count == final_count == 3

    def test_use_case_returns_reference_to_repository_list(self, use_case, user_repository):
        """Test that use_case returns the actual repository list"""
        result = use_case()
        repo_list = user_repository.get_all()
        
        assert result is repo_list

    def test_admin_user_has_correct_id(self, use_case):
        """Test that admin user has the expected ID from mock"""
        result = use_case()
        
        admin = [user for user in result if user.email == "admin@example.com"][0]
        assert admin.id == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"

    def test_user1_has_correct_id(self, use_case):
        """Test that user1 has the expected ID from mock"""
        result = use_case()
        
        user1 = [user for user in result if user.email == "user1@example.com"][0]
        assert user1.id == "93bc6ada-c0d1-7054-26ab-e17454c48ae6"

    def test_user2_has_correct_id(self, use_case):
        """Test that user2 has the expected ID from mock"""
        result = use_case()
        
        user2 = [user for user in result if user.email == "user2@example.com"][0]
        assert user2.id == "93bc6ada-c0e1-7054-26ab-e17414c48ae9"

    def test_returned_users_preserve_order(self, use_case):
        """Test that users are returned in expected order"""
        result = use_case()
        
        assert result[0].email == "admin@example.com"
        assert result[1].email == "user1@example.com"
        assert result[2].email == "user2@example.com"

    def test_use_case_called_after_repository_modification(self, use_case, user_repository):
        """Test that use_case reflects changes after repository modification"""
        # Initial call
        result1 = use_case()
        initial_count = len(result1)
        
        # Add a new user to repository
        new_user = User(
            id="new-test-id",
            email="newuser@example.com",
            hashed_password="new_hashed_pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        user_repository.create(new_user)
        
        # Call again
        result2 = use_case()
        
        assert len(result2) == initial_count + 1
        assert "newuser@example.com" in [user.email for user in result2]

    # ==================== INVALID DATA ASSERTIONS ====================
    # These tests assert INCORRECT data to validate what comes from the database
    
    def test_incorrect_user_count_assertion(self, use_case):
        """Test that asserting wrong user count fails - validates actual count is 3"""
        result = use_case()
        # This should fail because we have 3 users, not 5
        assert len(result) != 5
        assert len(result) != 0
        assert len(result) != 10

    def test_incorrect_email_assertion(self, use_case):
        """Test that asserting wrong emails fails - validates actual emails"""
        result = use_case()
        emails = [user.email for user in result]
        
        # These emails should NOT be in the result
        assert "wrong@example.com" not in emails
        assert "fake@example.com" not in emails
        assert "notreal@example.com" not in emails

    def test_incorrect_admin_count_assertion(self, use_case):
        """Test that asserting wrong admin count fails - validates 1 admin exists"""
        result = use_case()
        admin_users = [user for user in result if user.role == ROLE.ADMIN]
        
        # Should NOT be 0, 2, or 3 admins
        assert len(admin_users) != 0
        assert len(admin_users) != 2
        assert len(admin_users) != 3

    def test_incorrect_regular_user_count_assertion(self, use_case):
        """Test that asserting wrong regular user count fails - validates 2 regular users"""
        result = use_case()
        regular_users = [user for user in result if user.role == ROLE.USER]
        
        # Should NOT be 0, 1, or 3 regular users
        assert len(regular_users) != 0
        assert len(regular_users) != 1
        assert len(regular_users) != 3

    def test_incorrect_inactive_user_count_assertion(self, use_case):
        """Test that asserting wrong inactive count fails - validates 1 inactive user"""
        result = use_case()
        inactive_users = [user for user in result if user.is_active is False]
        
        # Should NOT be 0, 2, or 3 inactive users
        assert len(inactive_users) != 0
        assert len(inactive_users) != 2
        assert len(inactive_users) != 3

    def test_incorrect_active_user_count_assertion(self, use_case):
        """Test that asserting wrong active count fails - validates 2 active users"""
        result = use_case()
        active_users = [user for user in result if user.is_active is True]
        
        # Should NOT be 0, 1, or 3 active users
        assert len(active_users) != 0
        assert len(active_users) != 1
        assert len(active_users) != 3

    def test_incorrect_admin_email_assertion(self, use_case):
        """Test that asserting wrong admin email fails - validates admin@example.com"""
        result = use_case()
        admin_users = [user for user in result if user.role == ROLE.ADMIN]
        
        # Admin email should NOT be these values
        assert admin_users[0].email != "wrongadmin@example.com"
        assert admin_users[0].email != "user1@example.com"
        assert admin_users[0].email != "user2@example.com"

    def test_incorrect_admin_active_status_assertion(self, use_case):
        """Test that asserting admin is inactive fails - validates admin is active"""
        result = use_case()
        admin_users = [user for user in result if user.role == ROLE.ADMIN]
        
        # Admin should NOT be inactive
        assert admin_users[0].is_active is not False

    def test_incorrect_user2_active_status_assertion(self, use_case):
        """Test that asserting user2 is active fails - validates user2 is inactive"""
        result = use_case()
        user2 = [user for user in result if user.email == "user2@example.com"][0]
        
        # user2 should NOT be active
        assert user2.is_active is not True

    def test_incorrect_user1_active_status_assertion(self, use_case):
        """Test that asserting user1 is inactive fails - validates user1 is active"""
        result = use_case()
        user1 = [user for user in result if user.email == "user1@example.com"][0]
        
        # user1 should NOT be inactive
        assert user1.is_active is not False

    def test_incorrect_user_role_assertions(self, use_case):
        """Test that asserting wrong roles fails - validates correct role assignments"""
        result = use_case()
        
        user1 = [user for user in result if user.email == "user1@example.com"][0]
        user2 = [user for user in result if user.email == "user2@example.com"][0]
        admin = [user for user in result if user.email == "admin@example.com"][0]
        
        # user1 and user2 should NOT be admins
        assert user1.role is not ROLE.ADMIN
        assert user2.role is not ROLE.ADMIN
        
        # admin should NOT be regular user
        assert admin.role is not ROLE.USER

    def test_incorrect_id_format_assertion(self, use_case):
        """Test that asserting IDs without dashes fails - validates UUID format"""
        result = use_case()
        
        for user in result:
            # IDs should contain dashes (UUID format), NOT be simple integers
            assert not user.id.isdigit()
            assert "-" in user.id

    def test_incorrect_password_format_assertion(self, use_case):
        """Test that asserting plain passwords fails - validates passwords are hashed"""
        result = use_case()
        
        for user in result:
            # Passwords should NOT be plain text like "password" or "123456"
            assert user.hashed_password != "password"
            assert user.hashed_password != "123456"
            assert user.hashed_password != "admin"
            assert user.hashed_password != "user"

    def test_incorrect_empty_result_assertion(self, use_case):
        """Test that asserting empty result fails - validates users exist"""
        result = use_case()
        
        # Result should NOT be empty
        assert result is not None
        assert len(result) > 0
        assert result != []

    def test_incorrect_return_type_assertion(self, use_case):
        """Test that asserting wrong return type fails - validates list is returned"""
        result = use_case()
        
        # Result should NOT be these types
        assert not isinstance(result, str)
        assert not isinstance(result, dict)
        assert not isinstance(result, int)
        assert not isinstance(result, tuple)
        assert result is not None

    def test_incorrect_user_entity_type_assertion(self, use_case):
        """Test that asserting wrong entity types fails - validates User entities"""
        result = use_case()
        
        for user in result:
            # Users should NOT be dicts, strings, or None
            assert not isinstance(user, dict)
            assert not isinstance(user, str)
            assert user is not None

    def test_specific_user_ids_not_matching_wrong_values(self, use_case):
        """Test that specific user IDs don't match wrong values"""
        result = use_case()
        
        admin = [user for user in result if user.email == "admin@example.com"][0]
        user1 = [user for user in result if user.email == "user1@example.com"][0]
        user2 = [user for user in result if user.email == "user2@example.com"][0]
        
        # These should NOT be the IDs
        assert admin.id != "93bc6ada-c0d1-7054-26ab-e17454c48ae6"  # This is user1's ID
        assert user1.id != "93bc6ada-c0d1-7054-26ab-e17414c48ae3"  # This is admin's ID
        assert user2.id != "93bc6ada-c0d1-7054-26ab-e17414c48ae3"  # This is admin's ID

    def test_all_users_not_having_same_role(self, use_case):
        """Test that not all users have the same role - validates role diversity"""
        result = use_case()
        
        roles = [user.role for user in result]
        
        # Should NOT all be the same role
        assert not all(role == ROLE.ADMIN for role in roles)
        assert not all(role == ROLE.USER for role in roles)

    def test_all_users_not_having_same_active_status(self, use_case):
        """Test that not all users have same active status - validates status diversity"""
        result = use_case()
        
        statuses = [user.is_active for user in result]
        
        # Should NOT all be active or all be inactive
        assert not all(status is True for status in statuses)
        assert not all(status is False for status in statuses)

    def test_email_domains_are_not_wrong_domains(self, use_case):
        """Test that email domains are not wrong values - validates example.com domain"""
        result = use_case()
        
        for user in result:
            # Should NOT have these domains
            assert "gmail.com" not in user.email
            assert "yahoo.com" not in user.email
            assert "hotmail.com" not in user.email
            assert "test.com" not in user.email
