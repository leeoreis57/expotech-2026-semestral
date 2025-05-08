from utils.mysql import MySqlDatabase
from dto.products import ProductDto

class Products: 
  def __init__(self):
    self.db = MySqlDatabase()

  def register_product(self, data: ProductDto):
    sql = """
      INSERT INTO tbl_formula_produtos (nome_produto, qtd_necessaria, fk_materia_prima)
      VALUES (%s, %s, %s)
    """

    for item in data.formula:
      print(item)
      response = self.db.execute(sql, (data.name, item["quantity"], item["materia_prima_id"]))
      print(response)