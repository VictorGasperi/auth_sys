from app.shared.domain.enums.role import ROLE
from app.shared.environments import Environments
from app.shared.infra.repository.adapters.user_repository_pgsql import UserRepositoryPgsql

inst = UserRepositoryPgsql()
usr = inst.update(user_id="1234", new_email="victor@gmail.com", new_role=ROLE.USER)
print(usr)