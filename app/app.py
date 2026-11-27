from database import criar_tabela, preencher_dados_iniciais
from flask import Flask, redirect, render_template, request, session, url_for
from models import Administrador, Comum, Produto, Usuario

app = Flask(__name__)
app.secret_key = "essa_eh_minha_chave_secreta_para_criar_sessoes_de_usuario"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = Usuario.autenticar(
            request.form.get("email"), request.form.get("senha")
        )
        if not usuario:
            return render_template("login.html", erro="E-mail ou senha incorretos!")

        session["user_id"] = usuario.id
        session["user_nome"] = usuario.nome
        session["user_email"] = usuario.email
        session["user_perfil"] = usuario.perfil

        if usuario.perfil == "admin":
            return redirect(url_for("painel_admin"))
        elif usuario.perfil == "comum":
            return redirect(url_for("painel_comum"))

    return render_template("login.html", erro=None)


@app.route("/admin", methods=["GET", "POST"])
def painel_admin():
    if session.get("user_perfil") != "admin":
        return redirect(url_for("login"))

    erro = None
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        perfil = request.form.get("perfil", "")

        if not nome or not email or not senha or perfil not in ("admin", "comum"):
            erro = "Preencha todos os campos corretamente."
        elif Administrador.cadastrar_usuario(nome, email, senha, perfil):
            return redirect(url_for("painel_admin"))
        else:
            erro = "Não foi possível cadastrar o usuário (verifique se o e-mail já está em uso)."

    usuarios = Administrador.listar_usuarios()

    return render_template(
        "admin.html",
        usuarios=usuarios,
        nome=session.get("user_nome"),
        id=session.get("user_id"),
        erro=erro,
    )


@app.route("/admin/editar/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario(id_usuario):
    if session.get("user_perfil") != "admin":
        return redirect(url_for("login"))

    usuario = Administrador.encontrar_usuario_por_id(id_usuario)
    if not usuario:
        return redirect(url_for("painel_admin"))

    erro = None
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        perfil = request.form.get("perfil", "")

        if not nome or not email or perfil not in ("admin", "comum"):
            erro = "Preencha nome, e-mail e perfil válidos."
        elif id_usuario == session.get("user_id") and perfil != "admin":
            erro = "Você não pode alterar o próprio perfil para comum."
        elif Administrador.atualizar_usuario(id_usuario, nome, email, senha, perfil):
            if id_usuario == session.get("user_id"):
                session["user_nome"] = nome
                session["user_email"] = email
                session["user_perfil"] = perfil
            return redirect(url_for("painel_admin"))
        else:
            erro = "Não foi possível atualizar o usuário (verifique se o e-mail já está em uso)."

    return render_template(
        "editar_usuario.html",
        usuario=usuario,
        erro=erro,
        id=session.get("user_id"),
    )


@app.route("/admin/excluir/<int:id_usuario>", methods=["POST"])
def excluir_usuario(id_usuario):
    if session.get("user_perfil") != "admin":
        return redirect(url_for("login"))

    if id_usuario == session.get("user_id"):
        return render_template(
            "admin.html",
            usuarios=Administrador.listar_usuarios(),
            nome=session.get("user_nome"),
            id=session.get("user_id"),
            erro="Você não pode excluir a própria conta.",
        )

    Administrador.deletar_usuario(id_usuario)
    return redirect(url_for("painel_admin"))


@app.route("/comum", methods=["GET"])
def painel_comum():
    if session.get("user_perfil") != "comum":
        return redirect(url_for("login"))

    return render_template(
        "comum.html",
        nome=session.get("user_nome"),
        email=session.get("user_email"),
        id=session.get("user_id"),
        erro=None,
    )


@app.route("/comum/atualizar", methods=["POST"])
def atualizar_conta():
    if session.get("user_perfil") != "comum":
        return redirect(url_for("login"))

    id_usuario = session.get("user_id")
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()

    if not nome or not email:
        return render_template(
            "comum.html",
            nome=session.get("user_nome"),
            email=session.get("user_email"),
            id=id_usuario,
            erro="Preencha nome e e-mail.",
        )

    if Comum.atualizar_conta(id_usuario, nome, email):
        session["user_nome"] = nome
        session["user_email"] = email
        return redirect(url_for("painel_comum"))

    return render_template(
        "comum.html",
        nome=session.get("user_nome"),
        email=session.get("user_email"),
        id=id_usuario,
        erro="Não foi possível atualizar os dados (verifique se o e-mail já está em uso).",
    )


@app.route("/comum/alterar-senha", methods=["POST"])
def alterar_senha():
    if session.get("user_perfil") != "comum":
        return redirect(url_for("login"))

    id_usuario = session.get("user_id")
    nova_senha = request.form.get("nova_senha", "")

    if not nova_senha.strip():
        return render_template(
            "comum.html",
            nome=session.get("user_nome"),
            email=session.get("user_email"),
            id=id_usuario,
            erro="Informe uma nova senha válida.",
        )

    usuario = Comum(
        id_usuario,
        session.get("user_nome"),
        session.get("user_email"),
        "comum",
    )
    if usuario.alterar_senha(nova_senha):
        return render_template(
            "comum.html",
            nome=session.get("user_nome"),
            email=session.get("user_email"),
            id=id_usuario,
            erro=None,
            sucesso="Senha alterada com sucesso.",
        )

    return render_template(
        "comum.html",
        nome=session.get("user_nome"),
        email=session.get("user_email"),
        id=id_usuario,
        erro="Não foi possível alterar a senha.",
    )


@app.route("/comum/excluir", methods=["POST"])
def excluir_conta():
    if session.get("user_perfil") != "comum":
        return redirect(url_for("login"))

    id_usuario = session.get("user_id")
    Comum.excluir_conta(id_usuario)
    session.clear()
    return redirect(url_for("login"))


@app.route("/produtos", methods=["GET", "POST"])
def produtos():
    perfil = session.get("user_perfil")
    if perfil not in ("admin", "comum"):
        return redirect(url_for("login"))

    erro = None
    if request.method == "POST":
        if perfil != "admin":
            return redirect(url_for("login"))

        dados, erro = Produto.validar(
            request.form.get("nome"),
            request.form.get("preco"),
            request.form.get("quantidade"),
        )
        if not erro:
            nome, preco, quantidade = dados
            if Produto.cadastrar_produto(nome, preco, quantidade):
                return redirect(url_for("produtos"))
            erro = "Não foi possível cadastrar o produto."

    lista_produtos = Produto.listar_produtos()
    return render_template(
        "produtos.html",
        produtos=lista_produtos,
        nome=session.get("user_nome"),
        perfil=perfil,
        erro=erro,
    )


@app.route("/produtos/editar/<int:id_produto>", methods=["GET", "POST"])
def editar_produto(id_produto):
    if session.get("user_perfil") != "admin":
        return redirect(url_for("login"))

    produto = Produto.encontrar_produto_por_id(id_produto)
    if not produto:
        return redirect(url_for("produtos"))

    erro = None
    if request.method == "POST":
        dados, erro = Produto.validar(
            request.form.get("nome"),
            request.form.get("preco"),
            request.form.get("quantidade"),
        )
        if not erro:
            nome, preco, quantidade = dados
            if Produto.atualizar_produto(id_produto, nome, preco, quantidade):
                return redirect(url_for("produtos"))
            erro = "Não foi possível atualizar o produto."

    return render_template("editar_produto.html", produto=produto, erro=erro)


@app.route("/produtos/excluir/<int:id_produto>", methods=["POST"])
def excluir_produto(id_produto):
    if session.get("user_perfil") != "admin":
        return redirect(url_for("login"))

    Produto.deletar_produto(id_produto)
    return redirect(url_for("produtos"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    criar_tabela()
    preencher_dados_iniciais()
    app.run(debug=True)