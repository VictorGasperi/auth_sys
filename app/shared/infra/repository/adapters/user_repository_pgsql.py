from typing import List, Optional
import psycopg2
from psycopg2.extensions import cursor

from app.shared.domain.entities.user import User

from app.shared.domain.enums.role import ROLE
from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository
from app.shared.environments import Environments
from app.shared.utils.time_utils import dt_to_ms, ms_to_dt

def open_db_connection(func):
    def wrapper(self, *args, **kwargs):
        conn = psycopg2.connect(Environments.get_envs().pgsql_url)
        cur = conn.cursor()

        try:
            result = func(self, cur, *args, **kwargs)
            conn.commit()
            return result
        
        except Exception:
            conn.rollback()
            raise

        finally:
            cur.close()
            conn.close()
    return wrapper

class UserRepositoryPgsql(IUserRepository):
    
    @open_db_connection
    def get_by_id(self, cur: cursor, user_id: str) -> Optional[User]:
        cur.execute(
            """
                SELECT id, email, password_hash, role, is_active, created_at
                FROM main."user"
                WHERE id = %s
            """,
            (user_id,)
        )

        row = cur.fetchone()
        if row is None:
            return None
        
        return User(
            id=row[0],
            email=row[1],
            hashed_password=row[2],
            role=ROLE(row[3]),
            is_active=row[4],
            created_at_ms=dt_to_ms(row[5])
        )

    @open_db_connection
    def get_by_email(self, cur: cursor, email: str) -> User:
        cur.execute(
            """
                SELECT id, email, password_hash, role, is_active, created_at
                FROM main."user"
                WHERE email = %s
            """,
            (email,)
        )

        row = cur.fetchone()
        if row is None:
            return None
        
        return User(
            id=row[0],
            email=row[1],
            hashed_password=row[2],
            role=ROLE(row[3]),
            is_active=row[4],
            created_at_ms=dt_to_ms(row[5])
        )
    
    @open_db_connection
    def get_all(self, cur: cursor) -> List[User]:
        cur.execute(
            """
                SELECT id, email, password_hash, role, is_active, created_at
                FROM main."user"
            """
        )

        row = cur.fetchall()
        if row is None:
            return None

        users = [ User(
            id=u[0],
            email=u[1],
            hashed_password=u[2],
            role=ROLE(u[3]),
            is_active=u[4],
            created_at_ms=dt_to_ms(u[5]) )
            for u in row ]

        return users

    @open_db_connection
    def create(self, cur: cursor, user: User) -> User:

        date_in_db = ms_to_dt(user.created_at_ms)

        user_to_add = (user.id, user.email, user.hashed_password, user.role.value, user.is_active, date_in_db)

        cur.execute(
            """
                INSERT INTO main."user" (id, email, password_hash, role, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, email, password_hash, role, is_active, created_at
            """,
            user_to_add
        )

        row = cur.fetchone()
        return User(
            id=row[0],
            email=row[1],
            hashed_password=row[2],
            role=ROLE(row[3]),
            is_active=row[4],
            created_at_ms=dt_to_ms(row[5])
        )

    @open_db_connection
    def update(self, cur: cursor, user_id: str, new_email: Optional[str] = None, new_hashed_password: Optional[str] = None, new_role: Optional[ROLE] = None, new_is_active: Optional[bool] = None) -> User:
        fields = []
        values = []
    
        if new_email is not None:
            fields.append("email = %s")
            values.append(new_email)
    
        if new_hashed_password is not None:
            fields.append("password_hash = %s")
            values.append(new_hashed_password)
    
        if new_role is not None:
            fields.append("role = %s")
            values.append(new_role.value)
    
        if new_is_active is not None:
            fields.append("is_active = %s")
            values.append(new_is_active)
    
        values.append(user_id)
    
        query = f"""
            UPDATE main."user"
            SET {", ".join(fields)}
            WHERE id = %s
            RETURNING id, email, password_hash, role, is_active, created_at
        """
    
        cur.execute(query, tuple(values))
        row = cur.fetchone()
    
        return User(
            id=row[0],
            email=row[1],
            hashed_password=row[2],
            role=ROLE(row[3]),
            is_active=row[4],
            created_at_ms=dt_to_ms(row[5])
        )