import sqlite3
from sqlite3 import Connection, Error


class BD:
    @staticmethod
    def conectar() -> Connection | None:
        try:
            conexao = sqlite3.connect("educ4_data_base.db")
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao
        except Error as e:
            print(e)
            return None
    
    @staticmethod
    def criar_tabelas(queries: list[str]) -> bool:
        conexao = BD.conectar()

        if not conexao:
            return False
        
        try:
            cursor = conexao.cursor()
            
            for query in queries:
                cursor.execute(query)
                conexao.commit()
                
            return True
        except Error as e:
            print(e)
            return False
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def listar_tabelas() -> bool:
        conexao = BD.conectar()

        if not conexao:
            return False
        try:
            visualizar_tabelas = """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table';
            """
            cursor = conexao.cursor()
            cursor.execute(visualizar_tabelas)
            tabelas = cursor.fetchall()
            print(f"tabelas econtradas: {tabelas}\n")
            return True
        except sqlite3.Error as e:
            print(e)
            return False


def criar_tabelas() -> bool:
    """
    Criar todas as tabelas necessárias para o sistema funcionar adequadamente.
    """
    
    return BD.criar_tabelas(
        queries=[
            """
            CREATE TABLE IF NOT EXISTS perfil (
                id_perfil integer PRIMARY KEY,
                tipo_perfil  VARCHAR(100) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY,
                id_perfil INTEGER NOT NULL,
                nome TEXT NOT NULL,
                login VARCHAR(100) UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                FOREIGN KEY (id_perfil) REFERENCES perfil(id_perfil)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS alunos (
                id_aluno INTEGER PRIMARY KEY,
                matricula TEXT NOT NULL UNIQUE,
                id_usuario INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS professores (
                id_professor INTEGER PRIMARY KEY,
                id_usuario INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cursos (
                id_curso INTEGER PRIMARY KEY,
                id_professor INTEGER NOT NULL UNIQUE,
                nome_curso TEXT NOT NULL,
                carga_horaria INTEGER NOT NULL CHECK(carga_horaria > 0),
                descricao TEXT,
                FOREIGN KEY (id_professor) REFERENCES professores(id_professor)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS matriculas (
                id_aluno INTEGER NOT NULL,
                id_curso INTEGER NOT NULL,
                PRIMARY KEY(id_aluno, id_curso),
                FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
                FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS notas (
                id_aluno INTEGER NOT NULL,
                id_curso INTEGER NOT NULL,
                atividade_1 DECIMAL CHECK (atividade_1 BETWEEN 0 AND 10),
                atividade_2 DECIMAL CHECK (atividade_2 BETWEEN 0 AND 10),
                atividade_3 DECIMAL CHECk (atividade_3 BETWEEN 0 AND 10),
                trabalho_final DECIMAL CHECK (trabalho_final BETWEEN 0 AND 10),
                PRIMARY KEY(id_aluno,id_curso),
                FOREIGN KEY (id_aluno,id_curso) REFERENCES matriculas(id_aluno,id_curso)
            )
            """
            
        ]
    )

if __name__ == "__main__":
    if criar_tabelas():
        BD.listar_tabelas()
    else:
        print("bleh")