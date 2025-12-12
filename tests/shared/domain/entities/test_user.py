import pytest

from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE


class TestUser:
    def test_user_creation_with_all_fields(self):
        """Test creating a User instance with all fields"""
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="hashed_pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_pass"
        assert user.role == ROLE.USER
        assert user.is_active is True
        assert user.created_at_ms == 1000000

    def test_user_creation_with_admin_role(self):
        """Test creating a User with ADMIN role"""
        user = User(
            id="admin123",
            email="admin@example.com",
            hashed_password="admin_pass",
            role=ROLE.ADMIN,
            is_active=True,
            created_at_ms=1000000
        )
        
        assert user.role == ROLE.ADMIN
        assert user.email == "admin@example.com"

    def test_user_creation_inactive(self):
        """Test creating an inactive User"""
        user = User(
            id="user123",
            email="inactive@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=False,
            created_at_ms=1000000
        )
        
        assert user.is_active is False

    def test_user_to_dict_method(self):
        """Test converting User to dictionary"""
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="hashed_pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        user_dict = user.to_dict()
        
        assert "id" in user_dict
        assert "email" in user_dict
        assert "role" in user_dict
        assert "is_active" in user_dict
        assert "created_at_ms" in user_dict
        
        assert user_dict["email"] == "test@example.com"
        assert user_dict["role"] == ROLE.USER
        assert user_dict["is_active"] is True

    def test_user_to_dict_excludes_hashed_password(self):
        """Test that to_dict doesn't include hashed_password"""
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="hashed_pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        user_dict = user.to_dict()
        
        # to_dict should not include hashed_password
        assert "hashed_password" not in user_dict

    def test_user_attributes_exist(self):
        """Test User has all required attributes"""
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        assert hasattr(user, "id")
        assert hasattr(user, "email")
        assert hasattr(user, "hashed_password")
        assert hasattr(user, "role")
        assert hasattr(user, "is_active")
        assert hasattr(user, "created_at_ms")

    def test_user_email_field(self):
        """Test User email field"""
        email = "user@example.com"
        user = User(
            id="user123",
            email=email,
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        assert user.email == email

    def test_user_password_field(self):
        """Test User hashed_password field"""
        hashed_pass = "hashed_secure_password"
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password=hashed_pass,
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        assert user.hashed_password == hashed_pass

    def test_user_created_at_ms_field(self):
        """Test User created_at_ms field"""
        timestamp = 1609459200000  # 2021-01-01 in milliseconds
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=timestamp
        )
        
        assert user.created_at_ms == timestamp

    # Error scenario tests
    def test_user_missing_required_id(self):
        """Test that User requires id field"""
        with pytest.raises(Exception):
            User(
                email="test@example.com",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_missing_required_email(self):
        """Test that User requires email field"""
        with pytest.raises(Exception):
            User(
                id="user123",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_missing_required_hashed_password(self):
        """Test that User requires hashed_password field"""
        with pytest.raises(Exception):
            User(
                id="user123",
                email="test@example.com",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_missing_required_role(self):
        """Test that User requires role field"""
        with pytest.raises(Exception):
            User(
                id="user123",
                email="test@example.com",
                hashed_password="pass",
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_missing_required_created_at_ms(self):
        """Test that User requires created_at_ms field"""
        with pytest.raises(Exception):
            User(
                id="user123",
                email="test@example.com",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True
            )

    def test_user_invalid_role_type(self):
        """Test that invalid role type raises error"""
        with pytest.raises(Exception):
            User(
                id="user123",
                email="test@example.com",
                hashed_password="pass",
                role="invalid_role",
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_invalid_is_active_type(self):
        """Test that is_active type is coerced or handled by Pydantic"""
        # Pydantic 2.x coerces "yes" to True
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active="yes",  # Pydantic coerces this to True
            created_at_ms=1000000
        )
        # Pydantic may coerce "yes" to True
        assert isinstance(user.is_active, bool)

    def test_user_invalid_created_at_type(self):
        """Test that invalid created_at_ms type raises error"""
        with pytest.raises(Exception):
            User(
                id="user123",
                email="test@example.com",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms="invalid"
            )

    def test_user_none_id(self):
        """Test that None id raises error"""
        with pytest.raises(Exception):
            User(
                id=None,
                email="test@example.com",
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_none_email(self):
        """Test that None email raises error"""
        with pytest.raises(Exception):
            User(
                id="user123",
                email=None,
                hashed_password="pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=1000000
            )

    def test_user_to_dict_contains_all_fields(self):
        """Test that to_dict contains all expected fields"""
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="hashed_pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000
        )
        
        user_dict = user.to_dict()
        
        # Check all fields are present
        required_fields = ["id", "email", "role", "is_active", "created_at_ms"]
        for field in required_fields:
            assert field in user_dict, f"Field '{field}' missing from to_dict output"

    def test_user_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary"""
        user = User(
            id="user123",
            email="test@example.com",
            hashed_password="pass",
            role=ROLE.USER,
            is_active=True,
            created_at_ms=1000000        )
        
        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)