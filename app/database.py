import sqlite3
from sqlite3 import Error


### conexão com o banco de dados
def conectar():
    try:
        return sqlite3.connect("teste.db")
    except Error as e:
        print(e)
        return None


### criação das tabelas
def criar_tabela():
    try:
        conn = conectar()
        sql_create_usuarios_table = """ CREATE TABLE IF NOT EXISTS usuarios (
                                            id integer PRIMARY KEY,
                                            nome text NOT NULL,
                                            email text NOT NULL UNIQUE,
                                            senha text NOT NULL,
                                            perfil text NOT NULL
                                        ); """
        sql_create_produtos_table = """ CREATE TABLE IF NOT EXISTS produtos (
                                            id integer PRIMARY KEY,
                                            nome text NOT NULL,
                                            preco real NOT NULL,
                                            quantidade integer NOT NULL
                                        ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_usuarios_table)
        cursor.execute(sql_create_produtos_table)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


### dados iniciais do banco de dados
def preencher_dados_iniciais():

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO usuarios (id, nome, email, senha, perfil) VALUES (1, 'Admin', 'admin@admin.com', 'admin', 'admin')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO usuarios (id, nome, email, senha, perfil) VALUES (2, 'Comum', 'comum@comum.com', 'comum', 'comum')"
        )
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def autenticar_usuario(email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, email, perfil FROM usuarios WHERE email = ? and senha=?",
            (email, senha),
        )
        return cursor.fetchone()
    except Exception:
        return None
    finally:
        if conn:
            conn.close()


def cadastrar_usuario(nome, email, senha, perfil):

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, perfil) VALUES (?, ?, ?, ?)",
            (nome, email, senha, perfil),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def listar_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, perfil FROM usuarios")
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        if conn:
            conn.close()


def deletar_usuario(id_usuario):

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def atualizar_usuario(id_usuario, nome, email, senha, perfil):
    try:
        conn = conectar()
        cursor = conn.cursor()
        if senha == "":
            cursor.execute(
                "UPDATE usuarios SET nome = ?, email = ?, perfil = ? WHERE id = ?",
                (nome, email, perfil, id_usuario),
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET nome = ?, email = ?, senha = ?, perfil = ? WHERE id = ?",
                (nome, email, senha, perfil, id_usuario),
            )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def atualizar_senha(id_usuario, nova_senha):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE id = ?",
            (nova_senha, id_usuario),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def encontrar_usuario_por_id(id_usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, email, perfil FROM usuarios WHERE id = ?", (id_usuario,)
        )
        return cursor.fetchone()
    except Exception:
        return None
    finally:
        if conn:
            conn.close()


def cadastrar_produto(nome, preco, quantidade):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
            (nome, preco, quantidade),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def listar_produtos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, quantidade FROM produtos")
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        if conn:
            conn.close()


def deletar_produto(id_produto):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def atualizar_produto(id_produto, nome, preco, quantidade):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = ?, preco = ?, quantidade = ? WHERE id = ?",
            (nome, preco, quantidade, id_produto),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def encontrar_produto_por_id(id_produto):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, preco, quantidade FROM produtos WHERE id = ?", (id_produto,)
        )
        return cursor.fetchone()
    except Exception:
        return None
    finally:
        if conn:
            conn.close()