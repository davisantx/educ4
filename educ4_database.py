import sqlite3
from sqlite3 import Error

#conexão do BD
def conectar():
    try:
        conexao = sqlite3.connect("educ4_data_base.db")
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao
    except Error as e:
        print(e)
        return None


# tabelas

def tabela_perfil(conexao):
    try:
        sql_create_tabela_perfil = """
                CREATE TABLE IF NOT EXISTS perfil (
                    id_perfil integer PRIMARY KEY,
                    tipo_perfil  VARCHAR(100) UNIQUE NOT NULL
                )
        """
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_perfil)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)
        
def tabela_usuarios(conexao):
    try:
        sql_create_tabela_usuarios = """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY,
                    id_perfil INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    login VARCHAR(100) UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    FOREIGN KEY (id_perfil) REFERENCES perfil(id_perfil)
                    
                    
                )
        """
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_usuarios)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)


def tabela_alunos(conexao):
    try:
        sql_create_tabela_alunos = """
                CREATE TABLE IF NOT EXISTS alunos (
                    id_aluno INTEGER PRIMARY KEY,
                    matricula TEXT NOT NULL UNIQUE,
                    id_usuario INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                )
        """
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_alunos)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)
        
        
def tabela_professores(conexao):
    try:
        sql_create_tabela_professores = """
                CREATE TABLE IF NOT EXISTS professores (
                    id_professor INTEGER PRIMARY KEY,
                    id_usuario INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                )
        """
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_professores)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)
        
def tabela_cursos(conexao):
    try:
        sql_create_tabela_cursos = """
                CREATE TABLE IF NOT EXISTS cursos (
                    id_curso INTEGER PRIMARY KEY,
                    id_professor INTEGER NOT NULL UNIQUE,
                    nome_curso TEXT NOT NULL,
                    carga_horaria INTEGER NOT NULL CHECK(carga_horaria > 0),
                    descricao TEXT,
                    FOREIGN KEY (id_professor) REFERENCES professores(id_professor)
                )
        """
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_cursos)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)
        
        
        
def tabela_matriculas(conexao):
    try:
        sql_create_tabela_matriculas = """
                CREATE TABLE IF NOT EXISTS matriculas (
                    id_aluno INTEGER NOT NULL,
                    id_curso INTEGER NOT NULL,
                    PRIMARY KEY(id_aluno, id_curso),
                    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
                    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
                )
        """
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_matriculas)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)
        
def tabela_notas(conexao):
    try:
        sql_create_tabela_notas = """
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
        cursor = conexao.cursor()
        cursor.execute(sql_create_tabela_notas)
        conexao.commit()
    except sqlite3.Error as e:
        print(e)
    
    
# a criação das tabelas ta respeitando as dependencias das chaves estrangeiras
def criar_tabelas(conexao):
    tabela_perfil(conexao)
    tabela_usuarios(conexao)
    tabela_alunos(conexao)
    tabela_professores(conexao)
    tabela_cursos(conexao)
    tabela_matriculas(conexao)
    tabela_notas(conexao)
    
    
def listar_tabelas(conexao):
    try:
        olha_as_tabela = """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table';
        """
        cursor = conexao.cursor()
        cursor.execute(olha_as_tabela)
        tabelas = cursor.fetchall()
        print(f"tabelas econtradas: {tabelas}\n")
    except sqlite3.Error as e:
        print(e)
    
conexao = conectar()

print("Verificando conexão...")

if conexao is not None:
    print("Conexão estabelecida!")

    print("Criando tabelas...")
    criar_tabelas(conexao)

    print("Listando tabelas...")
    listar_tabelas(conexao)

    print("Finalizando...")
    conexao.close()
else:
    print("Falha na conexão!")