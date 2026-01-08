from app.shared.environments import Environments
from app.shared.infra.repository.adapters.user_repository_pgsql import UserRepositoryPgsql

inst = UserRepositoryPgsql()
usr = inst.get_by_id("1234")
print(usr)