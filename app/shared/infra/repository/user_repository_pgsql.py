from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository

'''
    Essa classe é o adapter para o banco de dados User dentro de PostgreSQL.
    É necessário criar um decorator externo, em outro arquivo, para que lide com as conexões com o banco de dados.
    A ideia é chamar o decorator antes de todas as funcoes e passar o cursor pra ela, lidando com try/catch no decorator.
    Antes de mais nada, será necessario criar a classe Environments, para puxar as variáveis de ambiente, e depois criar 
    o repositório de usuários mockado.
'''

class UserRepositoryPgsql(IUserRepository):
