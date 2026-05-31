import asyncio
import os

import bcrypt
from colorama import Fore
from utils.mysql import MySqlDatabase

PREFIX = "                    "


def limpar_tela():
    os.system("cls")


async def esperar_dashboard(perms, dashboard, user_id: int):
    await asyncio.sleep(2)
    return await dashboard(perms, user_id)


async def carregar_menu(perms: str, id: int, user_id: int):
    from main import dashboard, aguardar_login  # type: ignore
    db = MySqlDatabase()

    if id == 0:
        perms, user_id = await aguardar_login()
        return await dashboard(perms, user_id)

    # ─────────────────────────── ADMINISTRADOR ───────────────────────────
    if perms == "admin":
        match id:
            case 1:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Livros Cadastrados]{Fore.RESET}\n")
                livros = db.query("SELECT * FROM tbl_livros;", ())
                if livros:
                    for livro in livros:
                        print(f"{PREFIX}ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
                else:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro cadastrado.")
                await asyncio.sleep(10)
                return await esperar_dashboard(perms, dashboard, user_id)

            case 2:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Cadastro Livro]{Fore.RESET}\n")
                nome = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome do Livro:{Fore.RESET} ")
                autor = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Autor do Livro:{Fore.RESET} ")
                ano = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Ano do Livro:{Fore.RESET} ")
                genero = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Gênero do Livro:{Fore.RESET} ")
                quantidade = int(input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Quantidade:{Fore.RESET} "))

                result = db.execute(
                    "INSERT INTO tbl_livros (nome_livro, autor_livro, ano_livro, genero_livro, qnt_livro) VALUES (%s, %s, %s, %s, %s)",
                    (nome, autor, ano, genero, quantidade)
                )
                if result:
                    print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Livro cadastrado com sucesso!")
                else:
                    print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Erro ao cadastrar livro.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 3:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Excluir Livro]{Fore.RESET}\n")
                livros = db.query("SELECT id_livro, nome_livro, autor_livro, qnt_livro FROM tbl_livros", ())
                if not livros:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro cadastrado.")
                else:
                    for l in livros:
                        print(f"{PREFIX}ID: {l[0]} | Nome: {l[1]} | Autor: {l[2]} | Estoque: {l[3]}")
                    id_alvo = int(input(f"\n{PREFIX}{Fore.LIGHTYELLOW_EX}[?] ID do livro a excluir:{Fore.RESET} "))
                    confirmar = input(f"{PREFIX}{Fore.RED}[!]{Fore.RESET} Confirmar exclusão? <s/n>: ")
                    if confirmar.lower() == 's':
                        emprestimo_ativo = db.query(
                            "SELECT id_emprestimo FROM tbl_emprestimos WHERE id_livro = %s AND data_devolucao IS NULL",
                            (id_alvo,)
                        )
                        if emprestimo_ativo:
                            print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Livro possui empréstimo ativo. Aguarde a devolução antes de excluir.")
                        else:
                            db.execute("DELETE FROM tbl_favoritos WHERE id_livro = %s", (id_alvo,))
                            db.execute("DELETE FROM tbl_emprestimos WHERE id_livro = %s", (id_alvo,))
                            result = db.execute("DELETE FROM tbl_livros WHERE id_livro = %s", (id_alvo,))
                            if result:
                                print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Livro excluído com sucesso!")
                            else:
                                print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Erro ao excluir livro.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 4:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Empréstimos Ativos]{Fore.RESET}\n")
                emprestimos = db.query("""
                    SELECT u.nome_usuario, l.nome_livro, e.data_emprestimo
                    FROM tbl_emprestimos e
                    JOIN tbl_usuarios u ON e.id_leitor = u.id_usuario
                    JOIN tbl_livros l ON e.id_livro = l.id_livro
                    WHERE e.data_devolucao IS NULL
                """, ())
                if emprestimos:
                    for emp in emprestimos:
                        print(f"{PREFIX}Usuário: {emp[0]} | Livro: {emp[1]} | Empréstimo: {emp[2]}")
                else:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum empréstimo ativo no momento.")
                await asyncio.sleep(5)
                return await esperar_dashboard(perms, dashboard, user_id)

            case 5:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Empréstimo Manual]{Fore.RESET}\n")
                id_usuario = int(input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] ID do Usuário:{Fore.RESET} "))
                id_livro = int(input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] ID do Livro:{Fore.RESET} "))

                livro = db.query("SELECT qnt_livro FROM tbl_livros WHERE id_livro = %s;", (id_livro,))
                if not livro or livro[0][0] <= 0:
                    print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Livro indisponível no momento.")
                else:
                    db.execute("INSERT INTO tbl_emprestimos (id_livro, id_leitor) VALUES (%s, %s)", (id_livro, id_usuario))
                    db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro - 1 WHERE id_livro = %s", (id_livro,))
                    print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Empréstimo realizado com sucesso!")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 6:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Devolução de Livro]{Fore.RESET}\n")
                id_usuario = int(input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] ID do Usuário:{Fore.RESET} "))
                emprestimo = db.query(
                    "SELECT id_emprestimo, id_livro FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL;",
                    (id_usuario,)
                )
                if not emprestimo:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro emprestado para esse usuário.")
                else:
                    id_emprestimo, id_livro = emprestimo[0]
                    db.execute("UPDATE tbl_emprestimos SET data_devolucao = NOW() WHERE id_emprestimo = %s", (id_emprestimo,))
                    db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro + 1 WHERE id_livro = %s", (id_livro,))
                    print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Livro devolvido com sucesso.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 7:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Cadastro Usuário]{Fore.RESET}\n")
                nome = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome:{Fore.RESET} ")
                cpf = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] CPF:{Fore.RESET} ")
                telefone = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Telefone:{Fore.RESET} ")
                username = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome de usuário:{Fore.RESET} ")
                senha = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Senha:{Fore.RESET} ")

                hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                result = db.execute(
                    "INSERT INTO tbl_usuarios (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuario) VALUES (%s, %s, %s, %s, %s, 'leitor')",
                    (nome, cpf, telefone, username, hashed)
                )
                if result:
                    print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Usuário cadastrado com sucesso!")
                else:
                    print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Erro ao cadastrar usuário.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 8:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Excluir Usuário]{Fore.RESET}\n")
                usuarios = db.query(
                    "SELECT id_usuario, nome_usuario, username_usuario, tipo_usuario FROM tbl_usuarios",
                    ()
                )
                if not usuarios:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum usuário cadastrado.")
                else:
                    for u in usuarios:
                        print(f"{PREFIX}ID: {u[0]} | Nome: {u[1]} | Username: {u[2]} | Tipo: {u[3]}")
                    id_alvo = int(input(f"\n{PREFIX}{Fore.LIGHTYELLOW_EX}[?] ID do usuário a excluir:{Fore.RESET} "))
                    confirmar = input(f"{PREFIX}{Fore.RED}[!]{Fore.RESET} Confirmar exclusão? <s/n>: ")
                    if confirmar.lower() == 's':
                        emprestimo_ativo = db.query(
                            "SELECT id_emprestimo FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL",
                            (id_alvo,)
                        )
                        if emprestimo_ativo:
                            print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Usuário possui livro emprestado. Devolva antes de excluir.")
                        else:
                            db.execute("DELETE FROM tbl_favoritos WHERE id_usuario = %s", (id_alvo,))
                            db.execute("DELETE FROM tbl_emprestimos WHERE id_leitor = %s", (id_alvo,))
                            result = db.execute(
                                "DELETE FROM tbl_usuarios WHERE id_usuario = %s",
                                (id_alvo,)
                            )
                            if result:
                                print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Usuário excluído com sucesso!")
                            else:
                                print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Erro ao excluir usuário.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 9:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Cadastro Administrador]{Fore.RESET}\n")
                nome = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome:{Fore.RESET} ")
                telefone = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Telefone:{Fore.RESET} ")
                username = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome de usuário:{Fore.RESET} ")
                senha = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Senha:{Fore.RESET} ")

                existente = db.query(
                    "SELECT id_usuario FROM tbl_usuarios WHERE username_usuario = %s",
                    (username,)
                )
                if existente:
                    print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Username '{username}' já está em uso.")
                else:
                    hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    result = db.execute(
                        "INSERT INTO tbl_usuarios (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuario) VALUES (%s, %s, %s, %s, %s, 'admin')",
                        (nome, "", telefone, username, hashed)
                    )
                    if result:
                        print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Administrador '{username}' cadastrado com sucesso!")
                    else:
                        print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Erro ao cadastrar administrador.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case _:
                print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Opção inválida.")
                return await esperar_dashboard(perms, dashboard, user_id)

    # ─────────────────────────────── LEITOR ──────────────────────────────
    elif perms == "leitor":
        match id:
            case 1:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Ver/Pesquisar Livro]{Fore.RESET}\n")
                livros = db.query("SELECT * FROM tbl_livros;", ())
                if not livros:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro cadastrado.")
                    await asyncio.sleep(3)
                    return await esperar_dashboard(perms, dashboard, user_id)
                for livro in livros:
                    print(f"{PREFIX}ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
                print()
                termo = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Filtrar por NOME, ID ou GÊNERO (Enter para sair):{Fore.RESET} ").strip()
                if termo:
                    if termo.isdigit():
                        resultados = db.query("SELECT * FROM tbl_livros WHERE id_livro = %s;", (int(termo),))
                    else:
                        resultados = db.query("SELECT * FROM tbl_livros WHERE nome_livro LIKE %s OR genero_livro LIKE %s;", (f"%{termo}%", f"%{termo}%"))
                    print()
                    if resultados:
                        for livro in resultados:
                            print(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET} ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
                    else:
                        print(f"{PREFIX}{Fore.RED}[!]{Fore.RESET} Nenhum livro encontrado com o termo '{termo}'.")
                    await asyncio.sleep(5)
                return await esperar_dashboard(perms, dashboard, user_id)

            case 2:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Empréstimo de Livro]{Fore.RESET}\n")
                termo = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome ou ID do livro:{Fore.RESET} ")
                try:
                    resultado = db.query("SELECT * FROM tbl_livros WHERE nome_livro = %s OR id_livro = %s;", (termo, int(termo)))
                except ValueError:
                    resultado = db.query("SELECT * FROM tbl_livros WHERE nome_livro = %s;", (termo,))
                if resultado:
                    livro = resultado[0]
                    if livro[5] <= 0:
                        print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Livro indisponível no momento.")
                    else:
                        ja_tem = db.query(
                            "SELECT id_emprestimo FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL;",
                            (user_id,)
                        )
                        if ja_tem:
                            print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Você já tem um livro emprestado.")
                        else:
                            confirmar = input(f"{PREFIX}{Fore.YELLOW}[?]{Fore.RESET} Deseja emprestar '{livro[1]}' de {livro[2]}? <s/n>: ")
                            if confirmar.lower() == 's':
                                db.execute("INSERT INTO tbl_emprestimos (id_livro, id_leitor) VALUES (%s, %s)", (livro[0], user_id))
                                db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro - 1 WHERE id_livro = %s", (livro[0],))
                                print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Livro emprestado com sucesso!")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 3:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Devolução de Livro]{Fore.RESET}\n")
                emprestimo = db.query(
                    "SELECT id_emprestimo, id_livro FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL;",
                    (user_id,)
                )
                if not emprestimo:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro emprestado.")
                else:
                    id_emprestimo, id_livro = emprestimo[0]
                    db.execute("UPDATE tbl_emprestimos SET data_devolucao = NOW() WHERE id_emprestimo = %s", (id_emprestimo,))
                    db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro + 1 WHERE id_livro = %s", (id_livro,))
                    print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Livro devolvido com sucesso.")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 4:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Favoritar Livro]{Fore.RESET}\n")
                termo = input(f"{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome ou ID do livro:{Fore.RESET} ")
                try:
                    resultado = db.query("SELECT * FROM tbl_livros WHERE nome_livro = %s OR id_livro = %s;", (termo, int(termo)))
                except ValueError:
                    resultado = db.query("SELECT * FROM tbl_livros WHERE nome_livro LIKE %s;", (f"%{termo}%",))
                if not resultado:
                    print(f"{PREFIX}{Fore.RED}[!]{Fore.RESET} Nenhum livro encontrado.")
                else:
                    livro = resultado[0]
                    ja_favoritado = db.query(
                        "SELECT id_favorito FROM tbl_favoritos WHERE id_usuario = %s AND id_livro = %s;",
                        (user_id, livro[0])
                    )
                    if ja_favoritado:
                        print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} '{livro[1]}' já está nos seus favoritos.")
                    else:
                        db.execute(
                            "INSERT INTO tbl_favoritos (id_usuario, id_livro) VALUES (%s, %s)",
                            (user_id, livro[0])
                        )
                        print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} '{livro[1]}' adicionado aos favoritos!")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 5:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Desfavoritar Livro]{Fore.RESET}\n")
                favoritos = db.query("""
                    SELECT l.id_livro, l.nome_livro, l.autor_livro
                    FROM tbl_favoritos f
                    JOIN tbl_livros l ON f.id_livro = l.id_livro
                    WHERE f.id_usuario = %s;
                """, (user_id,))
                if not favoritos:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Você não tem livros favoritos para remover.")
                else:
                    for livro in favoritos:
                        print(f"{PREFIX}ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]}")
                    termo = input(f"\n{PREFIX}{Fore.LIGHTYELLOW_EX}[?] Nome ou ID do livro a desfavoritar:{Fore.RESET} ")
                    try:
                        resultado = db.query(
                            "SELECT id_livro FROM tbl_livros WHERE nome_livro = %s OR id_livro = %s;",
                            (termo, int(termo))
                        )
                    except ValueError:
                        resultado = db.query(
                            "SELECT id_livro FROM tbl_livros WHERE nome_livro LIKE %s;",
                            (f"%{termo}%",)
                        )
                    if not resultado:
                        print(f"{PREFIX}{Fore.RED}[!]{Fore.RESET} Livro não encontrado.")
                    else:
                        id_livro = resultado[0][0]
                        fav = db.query(
                            "SELECT id_favorito FROM tbl_favoritos WHERE id_usuario = %s AND id_livro = %s;",
                            (user_id, id_livro)
                        )
                        if not fav:
                            print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Este livro não está nos seus favoritos.")
                        else:
                            db.execute(
                                "DELETE FROM tbl_favoritos WHERE id_usuario = %s AND id_livro = %s",
                                (user_id, id_livro)
                            )
                            print(f"{PREFIX}{Fore.GREEN}[✓]{Fore.RESET} Livro removido dos favoritos!")
                return await esperar_dashboard(perms, dashboard, user_id)

            case 6:
                limpar_tela()
                print(f"{PREFIX}{Fore.LIGHTBLACK_EX}[BiblioTech - Meus Favoritos]{Fore.RESET}\n")
                favoritos = db.query("""
                    SELECT l.id_livro, l.nome_livro, l.autor_livro, l.ano_livro, l.genero_livro
                    FROM tbl_favoritos f
                    JOIN tbl_livros l ON f.id_livro = l.id_livro
                    WHERE f.id_usuario = %s;
                """, (user_id,))
                if favoritos:
                    for livro in favoritos:
                        print(f"{PREFIX}ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]}")
                else:
                    print(f"{PREFIX}{Fore.YELLOW}[!]{Fore.RESET} Você ainda não tem livros favoritos.")
                await asyncio.sleep(5)
                return await esperar_dashboard(perms, dashboard, user_id)

            case _:
                print(f"{PREFIX}{Fore.RED}[X]{Fore.RESET} Opção inválida.")
                return await esperar_dashboard(perms, dashboard, user_id)
