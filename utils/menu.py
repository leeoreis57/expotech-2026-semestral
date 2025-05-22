import os
import time
from colorama import Fore
from utils.mysql import MySqlDatabase


def limpar_tela():
    os.system("cls")


async def esperar_dashboard(perms, dashboard):
    time.sleep(2)
    return await dashboard(perms)


async def carregar_menu(perms: str, id: int, usuario: int):
    from main import dashboard, carregar_login
    db = MySqlDatabase()

    if id == 0:
        return carregar_login()

    # ------------------------- ADMINISTRADOR -------------------------
    if perms == "admin":
        match id:
            case 1:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Cadastro Livro]{Fore.RESET}\n")
                nome = input(f"{Fore.LIGHTYELLOW_EX}[?] Nome do Livro:{Fore.RESET} ")
                autor = input(f"{Fore.LIGHTYELLOW_EX}[?] Autor do Livro:{Fore.RESET} ")
                ano = input(f"{Fore.LIGHTYELLOW_EX}[?] Ano do Livro:{Fore.RESET} ")
                genero = input(f"{Fore.LIGHTYELLOW_EX}[?] Gênero do Livro:{Fore.RESET} ")
                quantidade = int(input(f"{Fore.LIGHTYELLOW_EX}[?] Quantidade:{Fore.RESET} "))

                result = db.execute(
                    "INSERT INTO tbl_livros (nome_livro, autor_livro, ano_livro, genero_livro, qnt_livro) VALUES (%s, %s, %s, %s, %s)",
                    (nome, autor, ano, genero, quantidade)
                )
                print(f"{Fore.GREEN}[✓]{Fore.RESET} Livro cadastrado com sucesso!" if result else f"{Fore.RED}[X]{Fore.RESET} Erro ao cadastrar livro.")
                return await esperar_dashboard(perms, dashboard)

            case 2:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Cadastro Usuário]{Fore.RESET}\n")
                nome = input(f"{Fore.LIGHTYELLOW_EX}[?] Nome:{Fore.RESET} ")
                cpf = input(f"{Fore.LIGHTYELLOW_EX}[?] CPF:{Fore.RESET} ")
                telefone = input(f"{Fore.LIGHTYELLOW_EX}[?] Telefone:{Fore.RESET} ")
                username = input(f"{Fore.LIGHTYELLOW_EX}[?] Nome de usuário:{Fore.RESET} ")
                senha = input(f"{Fore.LIGHTYELLOW_EX}[?] Senha:{Fore.RESET} ")

                result = db.execute(
                    "INSERT INTO tbl_usuarios (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuarior) VALUES (%s, %s, %s, %s, %s, 'leitor')",
                    (nome, cpf, telefone, username, senha)
                )
                print(f"{Fore.GREEN}[✓]{Fore.RESET} Usuário cadastrado com sucesso!" if result else f"{Fore.RED}[X]{Fore.RESET} Erro ao cadastrar usuário.")
                return await esperar_dashboard(perms, dashboard)

            case 3:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Livros Cadastrados]{Fore.RESET}\n")
                livros = db.query("SELECT * FROM tbl_livros;", ())
                for livro in livros:
                    print(f"ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
                time.sleep(10)
                return await dashboard(perms)

            case 4:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Empréstimos Ativos]{Fore.RESET}\n")
                emprestimos = db.query("""
                    SELECT u.nome_usuario, l.nome_livro, e.data_emprestimo 
                    FROM tbl_emprestimos e
                    JOIN tbl_usuarios u ON e.id_leitor = u.id_usuario
                    JOIN tbl_livros l ON e.id_livro = l.id_livro
                    WHERE e.data_devolucao IS NULL
                """, ())
                if emprestimos:
                    for emp in emprestimos:
                        print(f"Usuário: {emp[0]} | Livro: {emp[1]} | Empréstimo: {emp[2]}")
                else:
                    print(f"{Fore.YELLOW}[!]{Fore.RESET} Nenhum empréstimo ativo no momento.")
                return await esperar_dashboard(perms, dashboard)

            case 5:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Empréstimo Manual]{Fore.RESET}\n")
                id_usuario = int(input(f"{Fore.LIGHTYELLOW_EX}[?] ID do Usuário:{Fore.RESET} "))
                id_livro = int(input(f"{Fore.LIGHTYELLOW_EX}[?] ID do Livro:{Fore.RESET} "))

                livro = db.query("SELECT qnt_livro FROM tbl_livros WHERE id_livro = %s;", (id_livro,))
                if not livro or livro[0][0] <= 0:
                    print(f"{Fore.RED}[X]{Fore.RESET} Livro indisponível no momento.")
                else:
                    db.execute("INSERT INTO tbl_emprestimos (id_livro, id_leitor) VALUES (%s, %s)", (id_livro, id_usuario))
                    db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro - 1 WHERE id_livro = %s", (id_livro,))
                    print(f"{Fore.GREEN}[✓]{Fore.RESET} Empréstimo realizado com sucesso!")
                return await esperar_dashboard(perms, dashboard)

            case 6:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Devolução de Livro]{Fore.RESET}\n")
                id_usuario = int(input(f"{Fore.LIGHTYELLOW_EX}[?] ID do Usuário:{Fore.RESET} "))
                emprestimo = db.query("SELECT id_emprestimo, id_livro FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL;", (id_usuario,))
                if not emprestimo:
                    print(f"{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro emprestado para esse usuário.")
                else:
                    id_emprestimo, id_livro = emprestimo[0]
                    db.execute("UPDATE tbl_emprestimos SET data_devolucao = NOW() WHERE id_emprestimo = %s", (id_emprestimo,))
                    db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro + 1 WHERE id_livro = %s", (id_livro,))
                    print(f"{Fore.GREEN}[✓]{Fore.RESET} Livro devolvido com sucesso.")
                return await esperar_dashboard(perms, dashboard)

    # ------------------------- LEITOR -------------------------
    elif perms == "leitor":
        match id:
            case 1:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Empréstimo de Livro]{Fore.RESET}\n")
                termo = input(f'{Fore.LIGHTYELLOW_EX}[?] Nome ou ID do livro:{Fore.RESET} ')
                try:
                    resultado = db.query("SELECT * FROM tbl_livros WHERE nome_livro = %s OR id_livro = %s;", (termo, int(termo)))
                except ValueError:
                    resultado = db.query("SELECT * FROM tbl_livros WHERE nome_livro = %s;", (termo,))
                if resultado:
                    livro = resultado[0]
                    ja_tem = db.query("SELECT id_emprestimo FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL;", (usuario,))
                    if ja_tem:
                        print(f"{Fore.RED}[X]{Fore.RESET} Você já tem um livro emprestado.")
                    else:
                        confirmar = input(f"{Fore.YELLOW}[?]{Fore.RESET} Deseja emprestar '{livro[1]}' de {livro[2]}? <s/n>: ")
                        if confirmar.lower() == 's':
                            db.execute("INSERT INTO tbl_emprestimos (id_livro, id_leitor) VALUES (%s, %s)", (livro[0], usuario,))
                            db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro - 1 WHERE id_livro = %s", (livro[0],))
                            print(f"{Fore.GREEN}[✓]{Fore.RESET} Livro emprestado com sucesso!")
                return await esperar_dashboard (perms, dashboard)

            case 2:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Devolução de Livro]{Fore.RESET}\n")
                emprestimo = db.query("SELECT id_emprestimo, id_livro FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL;", (usuario,))
                if not emprestimo:
                    print(f"{Fore.YELLOW}[!]{Fore.RESET} Nenhum livro emprestado.")
                else:
                    id_emprestimo, id_livro = emprestimo[0]
                    db.execute("UPDATE tbl_emprestimos SET data_devolucao = NOW() WHERE id_emprestimo = %s", (id_emprestimo,))
                    db.execute("UPDATE tbl_livros SET qnt_livro = qnt_livro + 1 WHERE id_livro = %s", (id_livro,))
                    print(f"{Fore.GREEN}[✓]{Fore.RESET} Livro devolvido com sucesso.")
                return await esperar_dashboard(perms, dashboard)

            case 3:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Pesquisa de Livro]{Fore.RESET}\n")
                termo = input(f"{Fore.LIGHTYELLOW_EX}[?] Nome ou ID do livro:{Fore.RESET} ")
                if termo.isdigit():
                    query = "SELECT * FROM tbl_livros WHERE id_livro = %s;"
                    params = (int(termo),)
                else:
                    query = "SELECT * FROM tbl_livros WHERE nome_livro LIKE %s;"
                    params = (f"%{termo}%",)
                resultados = db.query(query, params)
                if resultados:
                    for livro in resultados:
                        print(f"\nID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]} | Quantidade: {livro[5]}")
                else:
                    print(f"{Fore.RED}[!]{Fore.RESET} Nenhum livro encontrado com o termo '{termo}'.")
                time.sleep(5)
                return await dashboard(perms)

            case 4:
                limpar_tela()
                print(f"{Fore.LIGHTBLACK_EX}[BookShell - Livros Cadastrados]{Fore.RESET}\n")
                livros = db.query("SELECT * FROM tbl_livros;", ())
                for livro in livros:
                    print(f"ID: {livro[0]} | Nome: {livro[1]} | Autor: {livro[2]} | Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
                time.sleep(10)
                return await dashboard(perms)