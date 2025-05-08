from mysql.connector import connect, Error

class MySqlDatabase:
  def __init__(self):
    self.connection = connect(
      host="localhost",
      user="roott",
      password="root",
      database="trabalho_faculdade"
    )

  def query(self, cmd: str):
    cursor = self.connection.cursor()
    cursor.execute(cmd)

    response = cursor.fetchall()
    cursor.close()
    self.connection.close()

    return response
  
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
