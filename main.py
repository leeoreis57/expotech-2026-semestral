import asyncio
import msvcrt
import os
import socket
import threading

import bcrypt
import uvicorn
import qrcode
from colorama import Fore, init

import state
from utils.menu import carregar_menu
from utils.mysql import MySqlDatabase

init(autoreset=True)

db = MySqlDatabase()


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def iniciar_servidor():
    uvicorn.run("backend.server:app", host="0.0.0.0", port=8000, log_level="error")


def exibir_qrcode(url: str):
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

def verificar_senha(senha_plain: str, senha_bd: str) -> bool:
    """Suporta senhas bcrypt (novas) e texto simples (legado)."""
    if senha_bd.startswith("$2b$") or senha_bd.startswith("$2a$"):
        return bcrypt.checkpw(senha_plain.encode("utf-8"), senha_bd.encode("utf-8"))
    return senha_plain == senha_bd


async def aguardar_login():
    """Clears screen, shows QR code, waits for mobile WS login or Enter for manual."""
    state.login_event.clear()
    state.register_event.clear()

    os.system("cls")
    ip = get_local_ip()
    url = f"http://{ip}:8000/join/start"
    print(f"\n{Fore.YELLOW}=== BiblioTech ===")
    print(f"{Fore.CYAN}Escaneie o QR Code para acessar pelo celular:\n")
    exibir_qrcode(url)
    print(f"{Fore.LIGHTBLACK_EX}Pressione Enter para fazer login manualmente.\n")

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key in ('\r', '\n'):
                print()
                return await login_manual()

        if state.register_event.is_set():
            state.register_event.clear()
            u = state.registered_user
            print(f"\n{Fore.CYAN}[+] Novo usuário registrado: {u['nome']} (@{u['username']})")

        if state.login_event.is_set():
            state.login_event.clear()
            perms = state.user_data["role"]
            user_id = state.user_data["user_id"]
            print(f"\n{Fore.GREEN}Login recebido pelo celular!")
            await asyncio.sleep(1)
            return perms, user_id

        await asyncio.sleep(0.1)


async def login_manual():
    print(f"{Fore.CYAN}=== LOGIN MANUAL ===")
    username = input("Usuário: ")
    senha = input("Senha: ")

    result = db.query(
        "SELECT id_usuario, tipo_usuario, senha_usuario FROM tbl_usuarios WHERE username_usuario = %s",
        (username,)
    )

    if result and verificar_senha(senha, result[0][2]):
        if not result[0][2].startswith("$2b$") and not result[0][2].startswith("$2a$"):
            hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            db.execute("UPDATE tbl_usuarios SET senha_usuario = %s WHERE id_usuario = %s", (hashed, result[0][0]))
        print(f"{Fore.GREEN}Login realizado com sucesso!")
        return result[0][1], result[0][0]
    else:
        print(f"{Fore.RED}Usuário ou senha inválidos.")
        return await aguardar_login()


async def dashboard(perms, user_id):
    print(f"\n{Fore.YELLOW}=== DASHBOARD ===")

    if perms == "admin":
        print("1 - Ver livros")
        print("2 - Cadastrar livro")
        print("3 - Excluir livro")
        print("4 - Ver empréstimos")
        print("5 - Empréstimo manual")
        print("6 - Devolução manual")
        print("7 - Cadastrar usuário")
        print("8 - Excluir usuário")
        print("9 - Cadastrar administrador")
        print("0 - Sair")

    elif perms == "leitor":
        print("1 - Ver/Pesquisar livro")
        print("2 - Emprestar livro")
        print("3 - Devolver livro")
        print("4 - Favoritar livro")
        print("5 - Desfavoritar livro")
        print("6 - Ver favoritos")
        print("0 - Sair")

    try:
        opcao = int(input("\nEscolha: "))
    except ValueError:
        print(f"{Fore.RED}Opção inválida. Digite um número.")
        await asyncio.sleep(1.5)
        return await dashboard(perms, user_id)
    await carregar_menu(perms, opcao, user_id)


async def iniciar():
    await asyncio.sleep(1)  # wait for uvicorn to be ready
    perms, user_id = await aguardar_login()
    await dashboard(perms, user_id)


if __name__ == "__main__":
    server_thread = threading.Thread(target=iniciar_servidor, daemon=True)
    server_thread.start()

    asyncio.run(iniciar())
