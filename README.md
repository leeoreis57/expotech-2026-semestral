# 📚 BiblioTech

> Sistema Inteligente de Gerenciamento de Biblioteca desenvolvido para a ExpoTech 2026.

## 📖 Sobre o Projeto

O **BiblioTech** é um sistema completo de gerenciamento de biblioteca desenvolvido em Python, integrando um painel administrativo via terminal com uma interface web acessível por dispositivos móveis.

O projeto foi criado para facilitar o controle de livros, usuários e empréstimos através de uma solução moderna, segura e acessível. O sistema utiliza comunicação em tempo real via WebSocket, autenticação segura e integração com banco de dados MySQL.

---

## 🎯 Objetivos

* Automatizar o gerenciamento de bibliotecas.
* Facilitar o controle de empréstimos e devoluções.
* Permitir acesso remoto por dispositivos móveis.
* Garantir segurança no armazenamento de usuários e senhas.
* Proporcionar uma experiência simples para administradores e leitores.

---

## 🚀 Funcionalidades

### 👨‍💼 Administrador

* Cadastro de livros
* Exclusão de livros
* Gerenciamento de usuários
* Visualização completa do acervo
* Controle de empréstimos
* Controle de devoluções

### 👨‍🎓 Leitor

* Consulta de livros disponíveis
* Pesquisa de livros
* Realização de empréstimos
* Devolução de livros
* Sistema de favoritos
* Gerenciamento da própria conta

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade                     |
| ---------- | ------------------------------ |
| Python     | Desenvolvimento principal      |
| FastAPI    | API e servidor web             |
| Uvicorn    | Execução do servidor           |
| WebSocket  | Comunicação em tempo real      |
| MySQL      | Banco de dados                 |
| PyMySQL    | Integração Python + MySQL      |
| HTML5      | Interface Web                  |
| CSS3       | Estilização                    |
| JavaScript | Interatividade                 |
| bcrypt     | Criptografia de senhas         |
| qrcode     | Geração de QR Code             |
| Colorama   | Interface colorida no terminal |

---

## 🏗️ Arquitetura do Sistema

O sistema inicia através do terminal Python.

1. O servidor FastAPI é iniciado automaticamente.
2. Um QR Code é gerado para acesso pelo celular.
3. O usuário acessa a tela de login.
4. A autenticação ocorre via WebSocket.
5. As informações são refletidas em tempo real no terminal.
6. O usuário utiliza as funcionalidades conforme seu perfil.

---

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza MySQL com as seguintes tabelas:

* Usuários
* Livros
* Empréstimos
* Favoritos

Relacionamentos garantem integridade dos dados e controle dos empréstimos realizados.

---

## 📂 Estrutura do Projeto

```text
biblioteca/
│
├── backend/
│   ├── server.py
│
├── utils/
│   ├── menu.py
│   ├── mysql.py
│
├── views/
│   ├── index.html
│
├── banco.sql
├── cadastrar_admin.py
├── main.py
├── state.py
└── README.md
```

## ⚙️ Instalação

### 1. Clonar o projeto

```bash
git clone https://github.com/leeoreis57/expotech-2026-semestral.git
```

### 2. Entrar na pasta

```bash
cd biblioteca
```

### 3. Instalar dependências

```bash
pip install fastapi uvicorn pymysql bcrypt colorama qrcode
```

### 4. Configurar o banco MySQL

Importe o arquivo:

```text
banco.sql
```

### 5. Executar o sistema

```bash
python main.py
```

---

## 🔒 Segurança

O sistema utiliza:

* Hash seguro de senhas com bcrypt
* Controle de acesso por perfil
* Validação de autenticação
* Comunicação em tempo real via WebSocket

---

## 📱 Acesso Mobile

Após iniciar o sistema, um QR Code é exibido no terminal.

Basta escanear o código com o celular para acessar a interface web de login.

---

## 👥 Equipe

Projeto desenvolvido para a **ExpoTech 2026**.

Integrantes:

* Leonardo Almeida
* (Adicionar demais integrantes)

---

## 🎓 Projeto Acadêmico

Desenvolvido como trabalho semestral para apresentação na ExpoTech 2026, demonstrando conhecimentos em:

* Desenvolvimento Backend
* Banco de Dados
* APIs Web
* WebSockets
* Segurança da Informação
* Integração Mobile
* Arquitetura de Sistemas

---

⭐ Se gostou do projeto, deixe uma estrela no repositório.
