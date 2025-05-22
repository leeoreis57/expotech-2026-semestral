import os
import time
import websockets
import asyncio
import json

from utils.menu import carregar_menu
from colorama import init, Fore

init(autoreset=True)
has_session = False
user_id = None

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_mensagem(titulo, mensagem, cor=Fore.RESET):
    print(f"""
    {Fore.LIGHTBLACK_EX}[BookShell - {titulo}]{Fore.RESET}
    
    {cor}{mensagem}{Fore.RESET}
    """)
    
async def carregar_login():
    global has_session, user_id
    os.system("cls")

    print(f"""
    {Fore.LIGHTBLACK_EX}[BookShell - Login]{Fore.RESET}
 
    {Fore.LIGHTBLACK_EX}Olá leitor, seja bem-vindo(a) à BookShell. Para darmos continuidade, realize seu login escaneando o QR CODE que vai aparecer na tela.{Fore.RESET}
    """)

    try:
        async with websockets.connect('wss://aff8-2804-41a0-3f06-5b00-80f6-c1cd-f58e-140e.ngrok-free.app') as websocket:
            await websocket.send(json.dumps({'action': 'terminal:start', 'terminalId': 'default'}))

            async for message in websocket:
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    print(f"{Fore.LIGHTRED_EX}Erro ao decodificar mensagem JSON.{Fore.RESET}")
                    continue

                action = data.get('action')

                if action == 'user:logged' and not has_session:
                    infos = data.get('payload', {})

                    has_session = True
                    user_id = infos.get('userId')

                    # Evitar conflito de aspas no print
                    print(f"    {Fore.LIGHTBLACK_EX}{infos.get('username', 'Usuário')}, sessão iniciada com sucesso! Aguarde para ser redirecionado(a).{Fore.RESET}")

                    time.sleep(1)
                    break
        await dashboard(infos.get('role', 'leitor'))

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Falha ao conectar com WebSocket: {e}{Fore.RESET}")
        
async def dashboard(perms: str):
    global has_session, user_id

    limpar_tela()

    menus = {
        "admin": [
            "Cadastrar Livro",
            "Cadastrar Leitor",
            "Listar Livros",
            "Listar Leitores",
            "Emprestar Livro",
            "Devolver Livro"
        ],
        "leitor": [
            "Emprestar Livro",
            "Devolver Livro",
            "Pesquisar Livro",
            "Listar Livros"
        ]
    }

    tipo_menu = "Administrativo" if perms == "admin" else "leitor"
    print(f"{Fore.LIGHTBLACK_EX}[BookShell - Menu {tipo_menu}]{Fore.RESET}\n")

    for idx, opcao in enumerate(menus[perms], 1):
        print(f"{Fore.LIGHTBLACK_EX}[{idx}]{Fore.RESET} {Fore.LIGHTYELLOW_EX}{opcao}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}[0]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Sair{Fore.RESET}\n")

    try:
        escolha = int(input(f"{Fore.LIGHTBLACK_EX}[?]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Deseja prosseguir com qual opção?{Fore.RESET} "))
        if escolha == 0:
            has_session = False
            user_id = None
            limpar_tela()
            exibir_mensagem("Sessão", "Você saiu da sessão. Redirecionando ao login...", Fore.LIGHTBLACK_EX)
            
            time.sleep(2)
            return await carregar_login()
          
        return await carregar_menu(perms, escolha, user_id)
    except ValueError:
        limpar_tela()
        
        exibir_mensagem("Alerta Menu", "Aceitamos apenas números no menu. Estamos te redirecionando em instantes...", Fore.LIGHTRED_EX)
        time.sleep(2)
        
        return await dashboard(perms)

if __name__ == "__main__":
    limpar_tela()

    asyncio.run(carregar_login())
