from mysql.connector import connect, Error

class MySqlDatabase:
  def __init__(self):
    self.connection = connect(
      host="20.206.250.192",
      user="edu",
      password="rootfoda",
      database="biblioteca"
    )

  def query(self, cmd: str, args: None):
    try: 
      # CRIANDO CONEXÃO COM O CURSOR
      cursor = self.connection.cursor()

      # EXECUTANDO O COMANDO
      cursor.execute(cmd, args or ())
      response = cursor.fetchall()

      # RETORNANDO CASO DE CERTO
      return response
    except Error as error:
      print(f"Erro ao executar o comando {cmd} -> {error}")
      return False
  
  def execute(self, cmd: str, args: None):
    try: 
      # CRIANDO CONEXÃO COM O CURSOR
      cursor = self.connection.cursor()

      # EXECUTANDO O COMANDO
      cursor.execute(cmd, args or ())
      self.connection.commit()

      # RETORNANDO CASO DE CERTO
      return True
    except Error as error:
      print(f"Erro ao executar o comando {cmd} -> {error}")
      return False
