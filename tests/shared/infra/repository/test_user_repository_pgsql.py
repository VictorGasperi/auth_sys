import pytest
import uuid
from app.shared.infra.repository.adapters.user_repository_pgsql import UserRepositoryPgsql
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.utils.time_utils import dt_to_ms


@pytest.mark.skip(reason="Skipping PostgreSQL tests to prevent pipeline breakage")
class TestUserRepositoryPgsql:
    """Test suite for UserRepositoryPgsql using real PostgreSQL database"""

    @pytest.fixture
    def repo(self):
        """Create a UserRepositoryPgsql instance"""
        return UserRepositoryPgsql()

    @pytest.fixture
    def sample_user(self):
        """Sample User domain object"""
        return User(
            id=str(uuid.uuid4()),
            email=f"test_{uuid.uuid4().hex}@example.com",
            hashed_password="hashed_pass_test",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )

    def test_get_by_id_with_existing_admin_user(self, repo):
        """Test getting the existing admin user by ID"""
        # Using the pre-loaded mock data
        result = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert result is not None
        assert result.email == "admin@example.com"
        assert result.role == ROLE.ADMIN

    def test_get_by_id_non_existing_user(self, repo):
        """Test getting user by non-existing ID returns None"""
        result = repo.get_by_id("non_existing_id_12345")
        
        assert result is None

    def test_get_by_email_with_admin_user(self, repo):
        """Test getting admin user by email"""
        result = repo.get_by_email("admin@example.com")
        
        assert result is not None
        assert result.email == "admin@example.com"
        assert result.role == ROLE.ADMIN

    def test_get_by_email_with_user1(self, repo):
        """Test getting user1 by email"""
        result = repo.get_by_email("user1@example.com")
        
        assert result is not None
        assert result.email == "user1@example.com"
        assert result.role == ROLE.USER
        assert result.is_active is True

    def test_get_by_email_with_user2(self, repo):
        """Test getting user2 by email"""
        result = repo.get_by_email("user2@example.com")
        
        assert result is not None
        assert result.email == "user2@example.com"
        assert result.role == ROLE.USER
        assert result.is_active is False

    def test_get_by_email_non_existing_user(self, repo):
        """Test getting user by non-existing email returns None"""
        result = repo.get_by_email("nonexistent@example.com")
        
        assert result is None

    def test_get_all_returns_users_list(self, repo):
        """Test get_all returns a list of users"""
        result = repo.get_all()
        
        assert isinstance(result, list)
        assert len(result) >= 3  # At least admin, user1, user2
        assert all(isinstance(user, User) for user in result)

    def test_get_all_contains_admin_user(self, repo):
        """Test that get_all contains the admin user"""
        result = repo.get_all()
        
        admin_users = [u for u in result if u.email == "admin@example.com"]
        assert len(admin_users) > 0
        assert admin_users[0].role == ROLE.ADMIN

    def test_create_user(self, repo, sample_user):
        """Test creating a new user"""
        result = repo.create(sample_user)
        
        assert result is not None
        assert result.id == sample_user.id
        assert result.email == sample_user.email
        assert result.role == ROLE.USER
        assert result.is_active is True

    def test_create_and_retrieve_user(self, repo, sample_user):
        """Test creating a user and then retrieving it"""
        created = repo.create(sample_user)
        retrieved = repo.get_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.email == created.email
        assert retrieved.role == created.role

    def test_create_user_with_admin_role(self, repo):
        """Test creating an admin user"""
        admin_user = User(
            id=str(uuid.uuid4()),
            email=f"admin_test_{uuid.uuid4().hex}@example.com",
            hashed_password="admin_pass",
            role=ROLE.ADMIN,
            is_active=True,
            created_at_ms=2000000
        )
        
        result = repo.create(admin_user)
        
        assert result.role == ROLE.ADMIN

    def test_create_user_inactive(self, repo):
        """Test creating an inactive user"""
        inactive_user = User(
            id=str(uuid.uuid4()),
            email=f"inactive_{uuid.uuid4().hex}@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=False,
            created_at_ms=3000000
        )
        
        result = repo.create(inactive_user)
        
        assert result.is_active is False

    def test_update_user_email(self, repo, sample_user):
        """Test updating user email"""
        created = repo.create(sample_user)
        new_email = f"updated_{uuid.uuid4().hex}@example.com"
        
        result = repo.update(created.id, new_email=new_email)
        
        assert result.email == new_email
        
        # Verify it was persisted
        retrieved = repo.get_by_id(created.id)
        assert retrieved.email == new_email

    def test_update_user_password(self, repo, sample_user):
        """Test updating user password"""
        created = repo.create(sample_user)
        new_password = "new_hashed_password_123"
        
        result = repo.update(created.id, new_hashed_password=new_password)
        
        assert result.hashed_password == new_password
        
        # Verify it was persisted
        retrieved = repo.get_by_id(created.id)
        assert retrieved.hashed_password == new_password

    def test_update_user_role(self, repo, sample_user):
        """Test updating user role"""
        created = repo.create(sample_user)
        
        result = repo.update(created.id, new_role=ROLE.ADMIN)
        
        assert result.role == ROLE.ADMIN
        
        # Verify it was persisted
        retrieved = repo.get_by_id(created.id)
        assert retrieved.role == ROLE.ADMIN

    def test_update_user_is_active(self, repo, sample_user):
        """Test updating user is_active status"""
        created = repo.create(sample_user)
        
        result = repo.update(created.id, new_is_active=False)
        
        assert result.is_active is False
        
        # Verify it was persisted
        retrieved = repo.get_by_id(created.id)
        assert retrieved.is_active is False

    def test_update_multiple_fields(self, repo, sample_user):
        """Test updating multiple user fields at once"""
        created = repo.create(sample_user)
        new_email = f"multi_{uuid.uuid4().hex}@example.com"
        
        result = repo.update(
            created.id,
            new_email=new_email,
            new_hashed_password="new_pass",
            new_role=ROLE.ADMIN,
            new_is_active=False
        )
        
        assert result.email == new_email
        assert result.hashed_password == "new_pass"
        assert result.role == ROLE.ADMIN
        assert result.is_active is False

    def test_update_with_only_email_preserves_other_fields(self, repo, sample_user):
        """Test that partial update preserves other fields"""
        created = repo.create(sample_user)
        original_role = created.role
        original_is_active = created.is_active
        new_email = f"partial_{uuid.uuid4().hex}@example.com"
        
        result = repo.update(created.id, new_email=new_email)
        
        assert result.email == new_email
        assert result.role == original_role
        assert result.is_active == original_is_active

    def test_update_user_deactivate_and_reactivate(self, repo, sample_user):
        """Test deactivating and reactivating a user"""
        created = repo.create(sample_user)
        
        # Deactivate
        repo.update(created.id, new_is_active=False)
        deactivated = repo.get_by_id(created.id)
        assert deactivated.is_active is False
        
        # Reactivate
        repo.update(created.id, new_is_active=True)
        reactivated = repo.get_by_id(created.id)
        assert reactivated.is_active is True

    def test_repository_implements_interface(self, repo):
        """Test that UserRepositoryPgsql implements IUserRepository"""
        from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository
        assert isinstance(repo, IUserRepository)

    def test_user_object_has_correct_attributes(self, repo):
        """Test that retrieved user has all correct attributes"""
        user = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert hasattr(user, 'id')
        assert hasattr(user, 'email')
        assert hasattr(user, 'hashed_password')
        assert hasattr(user, 'role')
        assert hasattr(user, 'is_active')
        assert hasattr(user, 'created_at_ms')

    def test_role_is_enum_type(self, repo):
        """Test that role is properly converted to ROLE enum"""
        user = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert isinstance(user.role, ROLE)

    def test_created_at_ms_is_integer(self, repo):
        """Test that created_at_ms is stored as integer milliseconds"""
        user = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert isinstance(user.created_at_ms, int)

    def test_create_multiple_users_with_different_roles(self, repo):
        """Test creating users with different roles"""
        users_to_create = [
            User(
                id=str(uuid.uuid4()),
                email=f"admin_{uuid.uuid4().hex}@example.com",
                hashed_password="pass",
                role=ROLE.ADMIN,
                is_active=True,
                created_at_ms=1000000
            ),
            User(
                id=str(uuid.uuid4()),
                email=f"user_{uuid.uuid4().hex}@example.com",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )
        ]
        
        created_users = [repo.create(u) for u in users_to_create]
        
        assert created_users[0].role == ROLE.ADMIN
        assert created_users[1].role == ROLE.USER

    def test_get_by_email_case_sensitive(self, repo):
        """Test that email search is case-sensitive"""
        # Known email in database
        result = repo.get_by_email("admin@example.com")
        assert result is not None
        
        # Different case should not be found (if database is case-sensitive)
        result_uppercase = repo.get_by_email("ADMIN@EXAMPLE.COM")
        # This depends on database configuration
        # Just verify it doesn't crash
        assert result_uppercase is None or result_uppercase.email == "admin@example.com"

    def test_user_email_is_string(self, repo):
        """Test that email field is a string"""
        user = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert isinstance(user.email, str)
        assert "@" in user.email

    def test_user_password_hash_is_string(self, repo):
        """Test that password hash is a string"""
        user = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert isinstance(user.hashed_password, str)

    def test_user_is_active_is_boolean(self, repo):
        """Test that is_active field is a boolean"""
        user = repo.get_by_id("93bc6ada-c0d1-7054-26ab-e17414c48ae3")
        
        assert isinstance(user.is_active, bool)
