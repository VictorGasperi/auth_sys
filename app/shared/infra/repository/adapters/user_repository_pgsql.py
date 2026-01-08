from typing import List, Optional
import psycopg2
from psycopg2.extensions import cursor

from app.shared.domain.entities.user import User

from app.shared.domain.enums.role import ROLE
from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository
from app.shared.environments import Environments
from app.shared.utils.time_utils import dt_to_ms

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
                FROM main.user
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
    def get_by_email(self, email: str) -> User:
        pass

    @open_db_connection
    def get_all(self) -> List[User]:
        pass

    @open_db_connection
    def create(self, user: User) -> User:
        pass

    @open_db_connection
    def update(self, user_id: str, new_email: Optional[str] = None, new_hashed_password: Optional[str] = None, new_role: Optional[ROLE] = None, new_is_active: Optional[bool] = None) -> User:
        pass
