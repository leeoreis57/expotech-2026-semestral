import os 

from colorama import init, Fore

if __name__ == "__main__":
  os.system("cls")
  init(autoreset=True)

  print(f"""
    {Fore.CYAN}[Gestão de Estoque com Prev. de P.A]{Fore.RESET}
  """)

  username = str(input(f"    {Fore.MAGENTA}Username:{Fore.RESET} "))
  password = str(input(f"    {Fore.MAGENTA}Senha:{Fore.RESET} "))

  if username != "admin" and password != "admin":
    os.system("cls")
    print(f"""
      {Fore.CYAN}[Gestão de Estoque com Prev. de P.A - 24/05/2025]{Fore.RESET}
      
      Username ou Senha inválidos.
    """)
  else: 
    os.system("cls")

    print(f"""
      {Fore.CYAN}[Gestão de Estoque com Prev. de P.A]{Fore.RESET}
          
      {Fore.BLUE}[1]{Fore.RESET} {Fore.YELLOW}Cadastrar Formula{Fore.RESET}
      {Fore.BLUE}[2]{Fore.RESET} {Fore.YELLOW}Cadastrar Produto{Fore.RESET}
      {Fore.BLUE}[3]{Fore.RESET} {Fore.YELLOW}Gerar Previsão de P.A{Fore.RESET}
      {Fore.BLUE}[4]{Fore.RESET} {Fore.YELLOW}Editar Produto{Fore.RESET}
    """)

    opcao = int(input(f"      {Fore.BLUE}[?]{Fore.RESET} {Fore.YELLOW}Selecione uma opção:{Fore.RESET} "))
    os.system("cls")
    
    print(f"      {Fore.CYAN}[Gestão de Estoque com Prev. de P.A]{Fore.RESET}")
    if opcao == 1:
      print("")
    elif opcao == 2:
      print("")
    elif opcao == 3: 
      print("")
    elif opcao == 4: 
      print("alska")
    else: 
      os.system("cls")