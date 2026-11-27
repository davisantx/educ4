class Usuario:
    def __init__(self, id: int, nome: str, login: str, senha: str):
        self.__id = id
        self.nome = nome
        self.login = login
        self.__senha = senha

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        """
        O que acontece sem esta função?
        ```python
        Traceback (most recent call last):
          File "/home/davisantx/code/educ4/app/models.py", line 48, in <module>
            usuario.id = 2
            ^^^^^^^^^^
        AttributeError: property 'id' of 'Usuario' object has no setter
        ```
        """
        pass

    @property
    def senha(self):
        return self.__senha

    def __str__(self) -> str:
        return f"ID: {self.__id} | nome: {self.nome} | login: {self.login} | senha: {self.senha}"

    @staticmethod
    def autenticar(email, senha) -> "Usuario | None":
        dados = db.autenticar_usuario(email, senha)
        if dados:
            id_u, nome, email, perfil = dados
            if perfil == "admin":
                return Administrador(id_u, nome, email, perfil)
            if perfil == "aluno":
                return Aluno(id_u, nome, email, perfil)
            if perfil == "professor":
                return Professor(id_u, nome, email, perfil)


class Administrador(Usuario):
    @staticmethod
    def cadastrar_usuario(nome, email, senha, perfil):
        return db.cadastrar_usuario(
            nome, email, senha, perfil
        )  # True se o cadastro for bem-sucedido, False caso contrário

    @staticmethod
    def listar_usuarios():
        usuarios = db.listar_usuarios()
        return [
            Administrador(id_u, nome, email, perfil)
            if perfil == "admin"
            else Comum(id_u, nome, email, perfil)
            for id_u, nome, email, perfil in usuarios
            if perfil in ("admin", "comum")
        ]

    @staticmethod
    def deletar_usuario(id_usuario):
        return db.deletar_usuario(
            id_usuario
        )  # True se a exclusão for bem-sucedida, False caso contrário

    @staticmethod
    def atualizar_usuario(id_usuario, nome, email, senha, perfil):
        return db.atualizar_usuario(
            id_usuario, nome, email, senha, perfil
        )  # True se a atualização for bem-sucedida, False caso contrário

    @staticmethod
    def encontrar_usuario_por_id(id_usuario) -> Usuario | None:
        dados = db.encontrar_usuario_por_id(id_usuario)
        if dados:
            id_u, nome, email, perfil = dados
            if perfil == "admin":
                return Administrador(id_u, nome, email, perfil)
            if perfil == "aluno":
                return Aluno(id_u, nome, email, perfil)
            if perfil == "professor":
                return Professor(id_u, nome, email, perfil)


class Aluno(Usuario):
    def __init__(self, matricula, cursos):
        self.__matricula = matricula
        self.__cursos = list[Curso]

    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, valor):
        pass

    @property
    def cursos(self):
        return self.__cursos

    @cursos.setter
    def cursos(self, valor): pass
        # self.__cursos = valor
        
    @staticmethod
    def listar_cursos(id_aluno: int):
        """
        Listar apenas os cursos de um aluno em específico
        """
        pass


class Professor(Usuario):
    pass


class Nota:
    def __init__(self, atividade_1, atividade_2, atividade_3, trabalho_final):
        self.__atividade_1 = atividade_1
        self.__atividade_2 = atividade_2
        self.__atividade_3 = atividade_3
        self.__trabalho_final = trabalho_final

    @property
    def atividade_1(self): return self.__atividade_1

    @property
    def atividade_2(self): return self.__atividade_2

    @property
    def atividade_3(self): return self.__atividade_3

    @property
    def trabalho_final(self): return self.__trabalho_final

    @property
    def media(self):
        return (self.__atividade_1 + self.__atividade_2 + self.__atividade_3 + self.__trabalho_final) / 4
    
class Curso:
    def __init__(
        self,
        nome: str,
        professor: Professor,
        carga_horaria: int,
        descricao: str,
        nota: Nota,
    ):
        self.__nome = nome
        self.__professor = professor
        self.__carga_horaria = carga_horaria
        self.__descricao = descricao
        self.__nota = nota

    @property
    def nome(self):
        return self.__nome

    def professor(self):
        return self.__professor

    @property
    def carga_horaria(self):
        return self.__carga_horaria

    @property
    def descricao(self):
        return self.__descricao

    @property
    def nota(self):
        return self.__nota
        
    
    @staticmethod
    def listar_cursos():
        """
        Listar todos os cursos cadastrados no sistema
        """
        produtos = db.listar_produtos()
        return [
            Produto(id_p, nome, preco, quantidade)
            for id_p, nome, preco, quantidade in produtos
        ]


if __name__ == "__main__":
    usuario = Usuario(1, "K", "A", "B")
    print(usuario)