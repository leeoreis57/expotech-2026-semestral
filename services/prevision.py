from dto.prevision import PrevisionDto
from utils.mysql import MySqlDatabase

class PrevisionStock: 
  def __init__(self):
    self.db = MySqlDatabase()

  def generate_prevision(self, data: PrevisionDto):
    print(data)