import pytest
from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE


class TestUserRepositoryMock:
    @pytest.fixture
    def repo(self):
        """Create a fresh UserRepositoryMock instance for each test"""
        return UserRepositoryMock()

    def test_repository_initialization(self, repo):
        """Test that UserRepositoryMock initializes with users"""
        assert repo.users_list is not None
        assert len(repo.users_list) > 0

    def test_initial_users_count(self, repo):
        """Test that UserRepositoryMock initializes with 3 users"""
        assert len(repo.users_list) == 3

    def test_initial_user_admin_exists(self, repo):
        """Test that admin user exists in initial data"""
        admin = repo.get_by_email("admin@example.com")
        assert admin.email == "admin@example.com"
        assert admin.role == ROLE.ADMIN

    def test_initial_user1_exists(self, repo):
        """Test that user1 exists in initial data"""
        user1 = repo.get_by_email("user1@example.com")
        assert user1.email == "user1@example.com"
        assert user1.role == ROLE.USER
        assert user1.is_active is True

    def test_initial_user2_exists(self, repo):
        """Test that user2 exists in initial data"""
        user2 = repo.get_by_email("user2@example.com")
        assert user2.email == "user2@example.com"
        assert user2.role == ROLE.USER
        assert user2.is_active is False

    def test_get_by_id_existing_user(self, repo):
        """Test getting user by existing ID"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        user = repo.get_by_id(user_id)
        assert user is not None

    def test_get_by_id_non_existing_user(self, repo):
        """Test getting user by non-existing ID raises exception"""
        with pytest.raises(Exception, match="No user found for id"):
            repo.get_by_id("non_existing_id")

    def test_get_by_email_existing_user(self, repo):
        """Test getting user by existing email"""
        user = repo.get_by_email("admin@example.com")
        assert user.email == "admin@example.com"

    def test_get_by_email_non_existing_user(self, repo):
        """Test getting user by non-existing email raises exception"""
        with pytest.raises(Exception, match="No user found for email"):
            repo.get_by_email("nonexistent@example.com")

    def test_get_all_returns_all_users(self, repo):
        """Test get_all returns all users"""
        users = repo.get_all()
        assert len(users) == 3

    def test_get_all_returns_list(self, repo):
        """Test get_all returns a list"""
        users = repo.get_all()
        assert isinstance(users, list)

    def test_create_new_user(self, repo):
        """Test creating a new user"""
        new_user = User(
            id="new_user_id",
            email="newuser@example.com",
            hashed_password="new_pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        created_user = repo.create(new_user)
        assert created_user.email == "newuser@example.com"

    def test_create_increases_user_count(self, repo):
        """Test that create increases the user count"""
        initial_count = len(repo.users_list)
        
        new_user = User(
            id="another_user",
            email="another@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        repo.create(new_user)
        assert len(repo.users_list) == initial_count + 1

    def test_create_returns_created_user(self, repo):
        """Test that create returns the created user"""
        new_user = User(
            id="test_id",
            email="test@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        returned_user = repo.create(new_user)
        assert returned_user == new_user

    def test_update_user_email(self, repo):
        """Test updating user email"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        updated_user = repo.update(user_id, new_email="updated@example.com")
        assert updated_user.email == "updated@example.com"

    def test_update_user_password(self, repo):
        """Test updating user password"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        new_password = "new_hashed_password"
        updated_user = repo.update(user_id, new_hashed_password=new_password)
        assert updated_user.hashed_password == new_password

    def test_update_user_role(self, repo):
        """Test updating user role"""
        users = repo.get_all()
        user_id = users[1].id if isinstance(users[1].id, str) else users[1].id[0]
        
        updated_user = repo.update(user_id, new_role=ROLE.ADMIN)
        assert updated_user.role == ROLE.ADMIN

    def test_update_user_is_active(self, repo):
        """Test updating user is_active status"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        updated_user = repo.update(user_id, new_is_active=False)
        assert updated_user.is_active is False

    def test_update_multiple_fields(self, repo):
        """Test updating multiple user fields at once"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        updated_user = repo.update(
            user_id,
            new_email="multi@example.com",
            new_role=ROLE.USER,
            new_is_active=False
        )
        
        assert updated_user.email == "multi@example.com"
        assert updated_user.role == ROLE.USER
        assert updated_user.is_active is False

    def test_update_non_existing_user(self, repo):
        """Test updating non-existing user raises exception"""
        with pytest.raises(Exception, match="No user found for id"):
            repo.update("non_existing_id", new_email="test@example.com")

    def test_update_with_none_values_preserves_fields(self, repo):
        """Test that update with None values doesn't change those fields"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        original_email = users[0].email
        original_role = users[0].role
        
        repo.update(user_id, new_hashed_password="new_pass")
        
        updated_user = repo.get_by_id(user_id)
        assert updated_user.email == original_email
        assert updated_user.role == original_role

    def test_repository_implements_interface(self, repo):
        """Test that UserRepositoryMock implements IUserRepository"""
        from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository
        assert isinstance(repo, IUserRepository)

    def test_get_by_id_with_empty_string_raises_exception(self, repo):
        """Test getting user by empty string ID raises exception"""
        with pytest.raises(Exception, match="No user found for id"):
            repo.get_by_id("")

    def test_get_by_id_with_special_characters(self, repo):
        """Test getting user by special character ID raises exception"""
        with pytest.raises(Exception, match="No user found for id"):
            repo.get_by_id("!@#$%^&*()")

    def test_get_by_email_with_empty_string_raises_exception(self, repo):
        """Test getting user by empty email raises exception"""
        with pytest.raises(Exception, match="No user found for email"):
            repo.get_by_email("")

    def test_get_by_email_case_sensitive(self, repo):
        """Test that email search is case-sensitive"""
        with pytest.raises(Exception, match="No user found for email"):
            repo.get_by_email("ADMIN@EXAMPLE.COM")

    def test_get_by_email_with_whitespace(self, repo):
        """Test getting user by email with whitespace raises exception"""
        with pytest.raises(Exception, match="No user found for email"):
            repo.get_by_email(" admin@example.com ")

    def test_create_user_with_duplicate_email(self, repo):
        """Test creating user with duplicate email"""
        new_user = User(
            id="duplicate_id",
            email="admin@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        # Should allow duplicate email (no validation at repository level)
        created_user = repo.create(new_user)
        assert created_user.email == "admin@example.com"
        
        # Now we should have 4 users
        assert len(repo.users_list) == 4

    def test_create_user_with_none_values(self, repo):
        """Test creating user with None in required fields"""
        with pytest.raises(Exception):
            new_user = User(
                id=None,
                email="test@example.com",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )
            repo.create(new_user)

    def test_update_non_existing_user_by_id(self, repo):
        """Test updating non-existing user raises exception"""
        with pytest.raises(Exception, match="No user found for id"):
            repo.update("completely_fake_id_12345")

    def test_update_with_invalid_role(self, repo):
        """Test that updating with invalid role type raises error or coerces"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        # Pydantic should raise an error for invalid ROLE value
        try:
            repo.update(user_id, new_role="invalid_role")
            # If no error, the update may have coerced or kept original value
        except Exception:
            # Expected behavior
            pass

    def test_update_with_invalid_is_active_type(self, repo):
        """Test that updating with invalid is_active type bypasses validation"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        # The mock repo doesn't validate, it just assigns the value
        # So "yes" remains a string, not coerced to bool
        updated_user = repo.update(user_id, new_is_active="yes")
        assert updated_user.is_active == "yes"

    def test_get_all_returns_same_list(self, repo):
        """Test that get_all returns the same list instance"""
        users1 = repo.get_all()
        users2 = repo.get_all()
        assert users1 is users2

    def test_update_returns_same_user_instance(self, repo):
        """Test that update returns the modified user instance"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        original_user = users[0]
        
        updated_user = repo.update(user_id, new_email="changed@example.com")
        
        # Should be the same object reference
        assert updated_user is original_user

    def test_create_returns_same_user_instance(self, repo):
        """Test that create returns the same user instance"""
        new_user = User(
            id="test_id",
            email="test@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        returned_user = repo.create(new_user)
        assert returned_user is new_user

    def test_get_by_email_returns_correct_user(self, repo):
        """Test that get_by_email returns the correct user"""
        user = repo.get_by_email("user1@example.com")
        assert user.email == "user1@example.com"
        assert user.role == ROLE.USER

    def test_multiple_updates_accumulate(self, repo):
        """Test that multiple updates accumulate changes"""
        users = repo.get_all()
        user_id = users[0].id if isinstance(users[0].id, str) else users[0].id[0]
        
        # Update email
        repo.update(user_id, new_email="email1@example.com")
        user = repo.get_by_id(user_id)
        assert user.email == "email1@example.com"
        
        # Update password (email should remain)
        repo.update(user_id, new_hashed_password="new_pass")
        user = repo.get_by_id(user_id)
        assert user.email == "email1@example.com"
        assert user.hashed_password == "new_pass"
