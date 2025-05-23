import os
import time
import websockets
import asyncio
import json
import qrcode
import shutil 
import keyboard

from utils.menu import carregar_menu
from colorama import init, Fore

init(autoreset=True)
has_session = False
user_id = None

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_mensagem(titulo, mensagem, cor=Fore.RESET):
    msg_centralizado(f"""
    {Fore.LIGHTBLACK_EX}[BookShell - {titulo}]{Fore.RESET}
    
    {cor}{mensagem}{Fore.RESET}
    """)

def msg_centralizado(texto: str):
    largura_terminal = shutil.get_terminal_size().columns
    linhas = texto.split('\n')
    
    for linha in linhas:
        linha = linha.strip()
        espacos = (largura_terminal - len(linha)) // 2
        if espacos < 0:
            espacos = 0
        print(' ' * espacos + linha)
        
def gerar_qrcode(data):
    qr = qrcode.QRCode(border=1)
    qr.add_data(data)
    qr.make(fit=True)
    
    matrix = qr.get_matrix()
    largura_terminal = shutil.get_terminal_size().columns

    for row in matrix:
        linha = ''.join('██' if cell else '  ' for cell in row)
        espacos = (largura_terminal - len(linha)) // 2
        print(' ' * espacos + linha)

async def carregar_login():
    global has_session, user_id
    os.system("cls")
    texto = f"""
    {Fore.LIGHTBLACK_EX}[BookShell - Login]{Fore.RESET}

    {Fore.LIGHTBLACK_EX}Olá leitor, seja bem-vindo(a) à BookShell. Para darmos continuidade, realize seu login escaneando o QR CODE que vai aparecer na tela.{Fore.RESET}
    """
    
    msg_centralizado(texto)
    try:
        async with websockets.connect('wss://bookshell.vmzt.wtf/ws') as websocket:
            await websocket.send(json.dumps({'action': 'terminal:start', 'terminalId': 'default'}))

            async for message in websocket:
                try:
                    data = json.loads(message)
                    action = data['action']
                    
                    if action == 'connection:opened':
                        gerar_qrcode(f'https://bookshell.vmzt.wtf/join/{data['sessionId']}')
                except json.JSONDecodeError:
                    print(f"{Fore.LIGHTRED_EX}Erro ao decodificar mensagem JSON.{Fore.RESET}")
                    continue

                action = data.get('action')

                if action == 'user:logged' and not has_session:
                    infos = data.get('payload', {})

                    has_session = True

                    # Evitar conflito de aspas no print
                    msg_centralizado(f"{Fore.LIGHTBLACK_EX}{infos.get('username', 'Usuário')}, sessão iniciada com sucesso! Aguarde para ser redirecionado(a).{Fore.RESET}")

                    time.sleep(1)
                    break
        await dashboard(infos.get('role', 'leitor'), infos.get('userId'))

    except Exception as e:
        msg_centralizado(f"{Fore.LIGHTRED_EX}Falha ao conectar com WebSocket: {e}{Fore.RESET}")
        
async def dashboard(perms: str, user_id: int):
    global has_session

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
    print(f"                    {Fore.LIGHTBLACK_EX}[BookShell - Menu {tipo_menu}]{Fore.RESET}\n")

    for idx, opcao in enumerate(menus[perms], 1):
        print(f"                    {Fore.LIGHTBLACK_EX}[{idx}]{Fore.RESET} {Fore.LIGHTYELLOW_EX}{opcao}{Fore.RESET}")
    print(f"                    {Fore.LIGHTBLACK_EX}[0]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Sair{Fore.RESET}\n")

    try:
        escolha = int(input(f"                    {Fore.LIGHTBLACK_EX}[?]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Deseja prosseguir com qual opção?{Fore.RESET} "))
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
        
        return await dashboard(perms, user_id)

if __name__ == "__main__":
    os.system("title BookShell - Beta")

    keyboard.press_and_release('alt+space')
    time.sleep(0.1) 
    keyboard.press_and_release('x')
    limpar_tela()

    # asyncio.run(dashboard('admin', 1))
    asyncio.run(carregar_login())
