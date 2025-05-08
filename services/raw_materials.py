from dto.raw_materials import RawMaterialsDto
from utils.mysql import MySqlDatabase 

class RawMaterialsServices: 
  def __init__(self):
    self.db = MySqlDatabase()

  def register_material(self, data: RawMaterialsDto):
    # INSERÇÃO DE DADOS
    sql = """ 
      INSERT INTO tbl_materias_primas (nome_material, unidade_material, quantidade_estoque)
      VALUES (%s, %s, %s)
    """ 

    # EXECUÇÃO DA INSERÇÃO
    res = self.db.execute(sql, (data.name, data.unity, data.quantity));
    
    # RESPOSTA DA INSERÇÃO
    if res: 
      return "Materia-prima cadastrada com sucesso."
    else: 
      return "Ocorreu um erro ao cadastrar uma materia-prima."
    
  def editar_material(self, data): 
    print(data)