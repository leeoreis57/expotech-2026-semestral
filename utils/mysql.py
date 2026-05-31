from pymysql import connect, MySQLError


class MySqlDatabase:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = connect(
                host="localhost",
                user="root",
                password="leleo",
                port=3306,
                database="biblioteca"
            )
        except Exception as e:
            print(f"[DB] Erro ao conectar ao banco de dados: {e}")
            self.connection = None

    def _ensure_connection(self):
        if self.connection is None:
            self._connect()
            return
        try:
            self.connection.ping(reconnect=True)
        except Exception:
            self._connect()

    def query(self, cmd: str, args: None):
        try:
            self._ensure_connection()
            if self.connection is None:
                print("[DB] Sem conexão com o banco de dados.")
                return False
            cursor = self.connection.cursor()
            cursor.execute(cmd, args or ())
            return cursor.fetchall()
        except MySQLError as error:
            print(f"Erro ao executar o comando {cmd} -> {error}")
            return False

    def execute(self, cmd: str, args: None):
        try:
            self._ensure_connection()
            if self.connection is None:
                print("[DB] Sem conexão com o banco de dados.")
                return False
            cursor = self.connection.cursor()
            cursor.execute(cmd, args or ())
            self.connection.commit()
            return True
        except MySQLError as error:
            print(f"Erro ao executar o comando {cmd} -> {error}")
            return False
