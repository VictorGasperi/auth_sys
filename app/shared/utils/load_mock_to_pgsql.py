from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock
from app.shared.infra.repository.adapters.user_repository_pgsql import UserRepositoryPgsql


def load_mock_to_pgsql():
    mock_list = UserRepositoryMock().users_list
    pgsql_inst = UserRepositoryPgsql()
    for u in mock_list:
        print("Inserindo o usuario " + u.id)
        pgsql_inst.create(u)
        print("Usuário inserido")

    print("Carregamento concluido!")

load_mock_to_pgsql()