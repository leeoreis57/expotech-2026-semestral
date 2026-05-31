import bcrypt
from utils.mysql import MySqlDatabase


def cadastrar_admin():
    print("=== Cadastrar Administrador ===\n")

    nome = input("Nome completo: ").strip()
    telefone = input("Telefone: ").strip()
    username = input("Username: ").strip()
    senha = input("Senha: ").strip()

    if not all([nome, telefone, username, senha]):
        print("Todos os campos são obrigatórios.")
        return

    db = MySqlDatabase()

    existente = db.query(
        "SELECT id_usuario FROM tbl_usuarios WHERE username_usuario = %s",
        (username,)
    )
    if existente:
        print(f"Username '{username}' já está em uso.")
        return

    hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    ok = db.execute(
        "INSERT INTO tbl_usuarios (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuario) VALUES (%s, %s, %s, %s, %s, 'admin')",
        (nome, "", telefone, username, hashed)
    )

    if ok:
        print(f"\nAdmin '{username}' cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar admin.")


if __name__ == "__main__":
    cadastrar_admin()
